import importlib.util
import unittest
from unittest.mock import Mock,patch

AVAILABLE=importlib.util.find_spec('fastapi') is not None

@unittest.skipUnless(AVAILABLE,'Backend dependencies are installed separately from static build tests')
class CommunicationTests(unittest.TestCase):
    def setUp(self):
        from multilingual import communications
        self.api=communications

    def test_anonymous_requests_are_rejected(self):
        for header in ['', 'Basic password', 'Bearer ']:
            with self.assertRaises(Exception) as result:self.api.user(header)
            self.assertEqual(result.exception.status_code,401 if header!='Bearer ' else 503)

    def test_room_membership_is_enforced(self):
        fake=Mock();fake.db.collection.return_value.document.return_value.get.return_value.to_dict.return_value={'participants':{'alice':'en'}}
        with patch.object(self.api,'cloud',return_value=fake):
            with self.assertRaises(Exception) as error:self.api.room_access('room123','mallory')
            self.assertEqual(error.exception.status_code,403)
            self.assertTrue(self.api.room_access('room123','alice'))

    def test_translation_failure_preserves_original(self):
        class Ref:
            data={}
            def create(self,value):self.data=value.copy()
            def update(self,value):self.data.update(value)
            def get(self):return self
            def to_dict(self):return self.data
        ref=Ref();room=Mock();room.collection.return_value.document.return_value=ref
        fake=Mock();fake.translate.side_effect=TimeoutError();fake.firestore.SERVER_TIMESTAMP='time'
        with patch.object(self.api,'cloud',return_value=fake),patch.object(self.api,'room_access',return_value=(room,{'participants':{'alice':'en','bob':'es'}})):
            result=self.api.save_message('room123','alice',self.api.Message(id='message123',text='Keep my original',language='en'))
        self.assertEqual(result['original'],'Keep my original')
        self.assertEqual(result['status'],'translation-unavailable')

    def test_unverified_speech_configuration_fails_closed(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(Exception) as error:self.api.speech_settings('hy')
            self.assertEqual(error.exception.status_code,503)

    def test_streaming_sdk_configuration_is_valid(self):
        from google.cloud import speech_v2
        request=speech_v2.StreamingRecognizeRequest(recognizer='projects/test/locations/us-central1/recognizers/_',streaming_config=speech_v2.StreamingRecognitionConfig(config=speech_v2.RecognitionConfig(explicit_decoding_config=speech_v2.ExplicitDecodingConfig(encoding='LINEAR16',sample_rate_hertz=16000,audio_channel_count=1),language_codes=['en-US'],model='chirp_3'),streaming_features=speech_v2.StreamingRecognitionFeatures(interim_results=True)))
        self.assertEqual(request.streaming_config.config.language_codes[0],'en-US')
