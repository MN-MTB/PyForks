from src.PyForks.trailforks_user import TrailforksUser

def test_get_data():
    tf_user = TrailforksUser(username="mnmtb")
    user_data = tf_user.get_user_info()
    print(user_data)
