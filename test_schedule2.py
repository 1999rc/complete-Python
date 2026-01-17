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
