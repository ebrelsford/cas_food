# encoding: utf-8
import csv
import re

from south.v2 import DataMigration

class Migration(DataMigration):

    numbered_school_pattern = re.compile('^[IPM]S (\d+)(.*)$')
    filename = '../data/Garden_to_Cafe.csv'

    def forwards(self, orm):
        "Import Garden to Cafe data."

        def _findSchool(name, borough):
            "Find school fuzzily with the given name and borough"
            numbered_school = self.numbered_school_pattern.match(name)
            if numbered_school:
                # try to find school using its number
                school_number = numbered_school.group(1)
                school_number = school_number.rjust(3, '0') # padded
                try:
                    school = orm.School.objects.get(borough=borough, name__icontains=school_number)
                    return school
                except:
                    remainder = numbered_school.group(2)
                    print "failed finding '%s' by number %s, trying with the remainder: '%s'" % (name, school_number, remainder)
                    name = remainder.strip()

            words = name.split()
            num_words = len(words)
            while num_words:
                try:
                    school = orm.School.objects.get(borough=borough, name__icontains=' '.join(words[:num_words]))
                    return school
                except:
                    num_words = num_words - 1
                    continue

            print "giving up finding school '%s'" % name
            return None

        gtcfile = csv.DictReader(open(self.filename, 'r'))
        for gtc in gtcfile:
            print gtc['School'], gtc['Garden Coordinators']
            school = _findSchool(gtc['School'], gtc['Boro'])
            if not school:
                print "Could not find '%s'" % gtc['School']
                continue

            gardenToCafe = orm.GardenToCafe(school=school, garden_coordinators=gtc['Garden Coordinators'], organization=gtc['Organization (if not school)'])
            gardenToCafe.save()

            school.participates_in_garden_to_cafe = True
            school.save()


    def backwards(self, orm):
        "Get rid of any trace of Garden to Cafe."
        orm.School.objects.filter(participates_in_garden_to_cafe=True).update(participates_in_garden_to_cafe=False)
        orm.GardenToCafe.objects.all().delete()


    models = {
        'schools.gardentocafe': {
            'Meta': {'object_name': 'GardenToCafe'},
            'garden_coordinators': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schools.School']"})
        },
        'schools.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'admin_district': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'geo_district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'has_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participates_in_garden_to_cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participates_in_wellness_in_the_schools': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']
