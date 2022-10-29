DROP TABLE audioapi_session
DROP TABLE audioapi_audio
DROP TABLE audioapi_audiouser
DROP TABLE django_session

DELETE FROM django_migrations WHERE app = 'audioapi'
DELETE FROM django_migrations WHERE app = 'sessions'