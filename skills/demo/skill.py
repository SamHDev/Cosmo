import cosmo.api as cosmo

api = cosmo.API()

class TestSkill(api.Skill):
    @api.IntentHandler(phrases=("time"))
    def time_intent_callback(self, msg):
        api.logger.debug(f"msg: {msg}")

api.register_skill(TestSkill)
