from django.db import models



class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/', blank=True)
    match_percentage = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'user'],
                name='unique_user_job_application'
            )
        ]

    def __str__(self):
        return self.name + " - " + self.job.title