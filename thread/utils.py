def sort_func(answer):
    sorted_answer = sum(
        [i.rating for i in answer.ratings.all()]) / answer.ratings.all().count()
    return sorted_answer
