
class RoundQuerySet(models.QuerySet):
    def score_total(self):
        return self.get_queryset().prefetch_related('shotdata').aggregate(Sum("shotdata__nr_strokes"))['shotdata__nr_strokes__sum']

    def putts_total(self):
        return self.prefetch_related('shotdata').aggregate(Sum("shotdata__nr_putts"))['shotdata__nr_putts__sum']

    def hole_average(self, num):
        return self.prefetch_related('shotdata').select_related('shotdata').filter(shotdata__hole__par=num).aggregate(Avg("shotdata__nr_strokes"))['shotdata__nr_strokes__avg']

    def score_percent(self, value):
        # Define the related query set.  Make it a little easier to read
        qs_related = self.prefetch_related(
            'shotdata').select_related('shotdata')

        round_holes = int(self.round_type)

        if value == 'par':
            return round((qs_related.filter(shotdata__nr_strokes=F('shotdata__hole__par')).count()/round_holes), 2)
        if value == 'birdie_better':
            return round((qs_related.filter(shotdata__nr_strokes__lt=F('shotdata__hole__par')).count()/round_holes), 2)
        if value == 'tbogey_worse':
            return round((qs_related.filter(shotdata__nr_strokes__gte=F('shotdata__hole__par')+3).count()/round_holes), 2)
        if isinstance(value, int):
            return round((qs_related.filter(shotdata__nr_strokes=F('shotdata__hole__par') + value).count()/round_holes), 2)
