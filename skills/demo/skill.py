import cosmo.api as cosmo

api = cosmo.API()

class TestSkill(api.Skill):
    @api.IntentHandler(phrases=["time"], arguments={"city": api.ArgumentType.String})
    def time_intent_callback(cosmo, msg):
        api.logger.debug(f"msg: {msg}")


api.register_skill(TestSkill)
