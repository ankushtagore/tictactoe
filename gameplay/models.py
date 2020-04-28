from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse

GAME_STATUS_CHOICES = (
    ('F', 'First Player to Move'),
    ('S', 'Second Player to Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)
class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(
            Q(first_player = user) | Q(second_player=user)
        )
    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )

class Game(models.Model):
    first_player = models.ForeignKey(User,
                                     related_name="games_first_player")
    second_player = models.ForeignKey(User,
                                      related_name="games_second_player")
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F',
                              choices=GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()


    def board(self):
        # return a 2d list of move obj, so u can ask for the state of a square in position [y][x]
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def get_absolute_url(self):                                     # it tells what canonical url is to django
        return reverse('gameplay_detail', args=[self.id])

    def __str__(self):
        return "{0} vs {1}".format(
            self.first_player, self.second_player)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    game = models.ForeignKey(Game, editable=False)
    by_first_player = models.BooleanField(editable=False)
