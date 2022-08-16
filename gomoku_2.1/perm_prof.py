from cprofile_graph import profile_decorator
from nine_nine_perm import rp_perm


@profile_decorator('prof.png')
def run():
    rp_perm(k=5)


if __name__ == '__main__':
    run()
