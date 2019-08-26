import cosmo.api as cosmo

api = cosmo.API()

class TestSkill(api.Skill):
<<<<<<< HEAD
    @api.IntentHandler(phrases=["time"], arguments={"city": api.ArgumentType.String})
    def time_intent_callback(cosmo, msg):
=======
    @api.IntentHandler(phrases=("time",))
    def time_intent_callback(self, msg):
>>>>>>> 73dab8c9fbbc9b6ae0e266bdb64540d1c4fba651
        api.logger.debug(f"msg: {msg}")


api.register_skill(TestSkill)
