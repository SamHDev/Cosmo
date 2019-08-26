import cosmo.api as cosmo

api = cosmo.API(debug=True)

class TestSkill(api.Skill):
    @api.Intent(phrases=("time",))
    def time_intent_callback(self,msg):
        api.logger.debug(f"msg: {msg}")