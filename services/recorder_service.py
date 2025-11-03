from models import Recorder, db

class RecorderService:
    @staticmethod
    def create_record(ipconfig, platform, browser):
        user = Recorder(client_ip=ipconfig, platform=platform, browser=browser)
        db.session.add(user)
        db.session.commit()
        return user
    @staticmethod
    def get_records():
        return Recorder.query.all()
    @staticmethod
    def delete_record(id):
        message = Recorder.query.get(id)
        db.session.delete(message)
        db.session.commit()
