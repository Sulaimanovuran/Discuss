from thread.models import Answer


def average_func(answer):
    try:
        sorted_answer = sum(
            [i.rating for i in answer.ratings.all()]) / answer.ratings.all().count()
        return sorted_answer
    except:
        sorted_answer = sum(
            [i.rating for i in answer.ratings.all()])
        return sorted_answer