from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from catalog.models import Author, Book, BookInstance, Genre
from django.views import generic
# Create your views here.


def index(request):
    # total number of books and book instances
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.count()
    # books with the letter a
    num_instances_avaliable = BookInstance.objects.filter(status__exact='a').count()
    # number of authors in the site
    num_authors = Author.objects.count()
    contains_genre = Genre.objects.filter(name__icontains='french').count()

    # number of visits to this view, as counted in teh session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_avaliable': num_instances_avaliable,
        'num_authors': num_authors,
        'contains_genre': contains_genre,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    template_name = 'templates/book_list.html'
    model = Book
    paginate_by = 5


class BookDetailView(generic.DetailView):
    template_name = 'templates/book_detail.html'
    model = Book


class AuthorListView(generic.ListView):
    template_name = 'templates/author_list.html'
    model = Author


class AuthorDetailView(generic.DetailView):
    template_name = 'templates/author_detail.html'
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'templates/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(status__exact='o').order_by('due_back')
