from copy_trading.models import CopyTrading
from signal_app.models import SignalType
from .models import Post
from forum.models import ForumQuestion


def monthly_signal():
    monthly_signal_qs = SignalType.objects.filter(signal_choice='Monthly')
    if monthly_signal_qs:
        monthly_signal = monthly_signal_qs.first()
    else:
        monthly_signal = None
    return monthly_signal


def quarterly_signal():
    quarterly_signal_qs = SignalType.objects.filter(signal_choice='Quarterly')
    if quarterly_signal_qs:
        quarterly_signal = quarterly_signal_qs.first()
    else:
        quarterly_signal = None
    return quarterly_signal


def yearly_signal():
    yearly_signal_qs = SignalType.objects.filter(signal_choice='Yearly')
    if yearly_signal_qs:
        yearly_signal = yearly_signal_qs.first()
    else:
        yearly_signal = None
    return yearly_signal


def add_variable_to_context(try_content=None):
    latest_posts = Post.objects.all()
    older_posts = Post.objects.all().order_by('id')
    if Post.objects.count() > 6:
        latest_posts = Post.objects.all()[3]
    if Post.objects.count() > 6:
        older_posts = Post.objects.all().order_by('id')[3]

    copy_trading = CopyTrading.objects.copy_trade_filter_choice('Monthly')
    top_forums = ForumQuestion.objects.top_forums()
    print('this is the top_forums hhh', top_forums)
    return {'older_posts': older_posts,
            'latest_posts': latest_posts,
            'instagram_url': 'http:instagram.com',
            'monthly_signal': monthly_signal,
            'quarterly_signal': quarterly_signal,
            'yearly_signal': yearly_signal,
            'top_forums': top_forums,
            # copy trading
            'copy_trade': copy_trading,
            }
