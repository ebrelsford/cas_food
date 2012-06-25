from getinvolved.models import Post

def promoted_posts(request):
    """
    Add promoted Get Involved posts.
    """
    # TODO cache?
    return {
        'promoted_posts': Post.objects.filter(promoted=True),
    }
