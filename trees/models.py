from django.db import models
from accounts.models import User
from datetime import datetime

class TreeManager(models.Manager):
    def validate(self, data):
        errors = {}
        species = data.get('species', '')
        location = data.get('location', '')
        notes = data.get('notes', '')
        date = data.get('date', '')
        zip_code = data.get('zip_code', '')

        if not species:
            errors['species'] = "species is required"
        
        if species and len(species) < 2:
            errors['species'] = "Species should be at least 2 characters"

        if not location:
            errors['location'] = "location is required"

        if location and len(location) < 5:
            errors['location'] = "Location should be at least 5 characters"

        date_obj = None

        if not date:
            errors['date'] = "Date is required."
        else:
            try:
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                errors['date'] = "Invalid date format."
        if date_obj:
            if date_obj > datetime.today().date():
                errors['date'] = "Date cannot be in the future."

        if not notes:
            errors['notes'] = "Notes field is required"

        if notes and len(notes) > 50:
            errors['notes'] = "notes should be at maximum 50 characters"
        
        if not zip_code:
            errors['zip_code'] = 'Zip Code is required'

        elif not zip_code.isdigit() or len(zip_code) != 5:
            errors['zip_code'] = "Zip Code should be a 5 digit number"

        return errors

    def create_tree(self, data, user):
        species = data.get('species', '')
        location = data.get('location', '')
        notes = data.get('notes', '')
        date = data.get('date', '')
        zip_code = data.get('zip_code', '')

        return self.create(species=species, location=location, notes=notes, date=date, creator=user, zip_code=zip_code)


class Tree(models.Model):
    species = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    date = models.DateField()
    creator = models.ForeignKey(User, related_name="trees", on_delete=models.CASCADE)
    notes = models.TextField()
    zip_code=models.CharField(max_length=10)
    visitors = models.ManyToManyField(User, related_name="visited_trees", through="Visiting")
    objects = TreeManager()

    def edit(self, data):
        species = data.get('species', '')
        location = data.get('location', '')
        notes = data.get('notes', '')
        date = data.get('date', '')
        zip_code = data.get('zip_code', '')


        self.species = species
        self.location = location
        self.notes = notes
        self.date = date
        self.zip_code = zip_code

        self.save()

        return self


# Optional Class (useful when add extra field for many to many relationship)
class Visiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    visited_at = models.DateField(null=True)
