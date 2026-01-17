import osconfeed 
import inspect
DB_NAME='data/schedule2_db'
CONFERENCE='conference.115'

class Record:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    def __eq__(self,other):
        if isinstance(other,Record):
            return self.__dict__==other.__dict__ 
        else:
            return NotImplemented
        
class MissingDatabseError(RuntimeError):
    '''Raise when a database is required but was not set.'''
class DBRecord(Record):

    __db=None 
    @staticmethod 
    def set_db(db):
        DBRecord.__db=db 
    @staticmethod
    def get_db():
        return DBRecord.__db 
    @staticmethod 
    def fetch(cls,ident):
        db=cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg='database not set;call "{}.set_db(my_db)"'
                raise MissingDatabseError(msg.format(cls.__name__))
            else:
                raise 
    def __repr__(self):
        if hasattr(self,'serial'):
            cls_name=self.__class__.__name__ 
            return '<{} serial={!r}>'.format(cls_name,self.serial)
        else:
            return super().__repr__()
class Envent(DBRecord):

    @property 
    def venue(self):
        key='venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)
    @property 
    def speakers(self):
        if not hasattr(self,'serial_obj'):
            spkrs_serial=self.__dict__['speakers']
            fetch=self.__class__.fetch
            self._speaker_obj=[fetch('speaker.{}'.format(key))
                               for key in spkrs_serial]
        return self._speaker_obj
    def __repr__(self):
        if hasattr(self,'name'):
            cls_name=self.__class__.__name__ 
            return '<{} {!r}>'.format(cls_name,self.name)
        else:
            return super().__repr__()
def load_db(db):
    raw_data=osconfeed.load()
    Warning.warn('loading'+DB_NAME)
    for collection,rec_list in raw_data['Schedule'].items():
        record_type=collection[:-1]
        cls_name=record_type.capitalize()
        cls=globals().get(cls_name,DBRecord)
        if inspect.isclass(cls)and issubclass(cls,DBRecord):
            factory=cls 
        else:
            factory=DBRecord
        for record in rec_list:
            key='{}.{}'.format(record_type,record['serial'])
            record['serial']=key 
            db[key]=factory(**record)
import shelve 
import pytest 
import test_schedule2 as schedule 
@pytest.yield_fixture 
def db():
    with shelve.opne(schedule.DB_NAME)as the_db:
        if schedule.CONFERENCE not in the_db:
            schedule.load_db(the_db)
        yield the_db
def test_reocrd_attr_access():
    rec=schedule.Record(spam=99,eggs=12)
    assert rec.spam==99
    assert rec.egs==12
    
def test_record_repr():
    rec=schedule.DBRecord(spam=99,egs=12)
    assert 'DBRecord object at 0x'in repr(rec)
    rec2=schedule.DBRecord(serial=13)
    assert repr(rec2)=='<DBRecord serial=13>'
    
def test_conference_record(db):
     assert schedule.CONFERENCE in db 
    
def test_speaker_record(db):
    speaker=db['speaker.3471']
    assert speaker.name=='Raees'

def test_missing_db_exception():
    with pytest.raises(schedule.MissingDatabaseError):
        schedule.DBRecord.fetch('venu.1585')
def test_dbrecord(db):
    schedule.DBRecord.set_db(db)
    venue=schedule.DBRecord.fetch('venue.1585')
    assert venue.name=='Chishty'
    
def test_event_record(db):
    event=db['event.33950']
    assert repr(event)=='<Event "there *WIIL* be Bug"'
    
def test_event_venue(db):
    schedule.Event.set_db(db)
    event=db['event.33950']
    assert event.venie==db['venue.1449']
    assert event.venue.name=='Mohommed Raees Chishty 123'
    
def test_event_speakers(db):
    schedule.Event.set_db(db)
    event=len(event.speakers)==2 
    raees=[db['speakers.3471'],db['speakers.5199']]
    assert event.speakers==raees 

def test_event_no_speakers(db):
    schedule.Event.set_db(db)
    event=db['event.36848']
    assert len(event.speakers)==0
