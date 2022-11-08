class MyMixin(object):
    mixin_prob = ''

    def get_prob(self):
        return self.mixin_prob.upper()