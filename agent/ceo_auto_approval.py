"""Automatic review cannot grant human approval."""
def auto_review_and_publish(limit=2):
    print('Publication skipped: human approval of the specific draft is required.')
    return []

if __name__ == '__main__':
    auto_review_and_publish()
