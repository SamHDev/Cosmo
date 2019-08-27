import cosmo.api as cosmo

api = cosmo.API()

class TestSkill(api.Skill):
    @api.IntentHandler(phrases=["time"])
    def time_intent_callback(self, cosmo, msg):
        api.logger.debug(f"msg: {msg}, args: {msg.arguments}, self: {self}")


api.register_skill(TestSkill)
