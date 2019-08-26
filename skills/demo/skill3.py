import cosmo.api as cosmo

api = cosmo.API(debug=True)

class TestSkill(api.Skill):
    def setup(self):
        print("!!!!!!!! wut")
        self.logger.debug("Started")

    @api.Intent(phrases=("time",))
    def time_intent_callback(self,*args,**kwargs):
        api.logger.debug(f"args: {args}. kwargs: {kwargs}")


api.register_skill(TestSkill)