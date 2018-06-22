from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookModelForm

# Create your views here.
def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(
        request,
        'index.html',
        context={
                 'num_books':num_books,'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors, 'num_visits':num_visits,
                 },
    )
class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/borrowed_books_list.html'
    model = BookInstance
    paginated_by = 2
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
class BookDetailView(generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
class AuthorDetailView(generic.DetailView):
    model = Author
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 1
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookModelForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data 
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        proposed_due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_due_back,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12.10.2016',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
class BookCreate(CreateView):
    model = Book 
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
class BookUpdate(UpdateView):
    model = Book
    fields = ['summary', 'genre']
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
