class NotEnoughPosts(RuntimeError):
    def __init__(self, intended, obtained):
        message = f'There are not enough posts. Only able to get {obtained} posts out of the {intended} intended.'
        super(NotEnoughPosts, self).__init__(message)
        self.message = message
