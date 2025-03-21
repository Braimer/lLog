from django.shortcuts import render,redirect,get_object_or_404
from .models import Topic,Entry    #retrieving data from database and sends to template
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    '''the home page for logs'''
    return render(request,'index.html')
    #return HttpResponse('hello mr braimer')
@login_required
def topics(request):
    '''show all topics'''
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'topics.html',context)

@login_required
def topic(request,topic_id):
    '''show a single topic and all its entries'''
    topic=Topic.objects.get(id=topic_id)### queris database for specific information
    #make sure the topic belongs to current user
    if topic.owner !=request.user:
        raise Http404
    
    entries=topic.entry_set.order_by('-date_added')###
    context={'topic':topic,'entries':entries}
    return render(request,'topic.html',context)

@login_required
def new_topic(request):
    '''add a new topic'''
    if request.method !='POST':
        #no data submitted ,create a blank form
        form=TopicForm()
    else:
        #POST submitted, process data
        form=TopicForm(data=request.POST)
        if form.is_valid():
            #fix intergrity error
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('logs:topics')
    #display a blank or invalid form
    context={'form':form}
    return render(request,'new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    '''add a new entry for a particular topic'''
    topic=Topic.objects.get(id=topic_id)
    if request.method !='POST':
        #no data submitted, create a blank form
        form=EntryForm()
    else:
        #POST data submitted ,process data
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('logs:topic',topic_id=topic_id)
    #display a blank or invalid form
    context={'topic':topic,'form':form}
    return render(request,'new_entry.html',context)


@login_required
def edit_entry(request,entry_id):
    '''edit an existing entry'''
    entry=get_object_or_404(Entry,id=entry_id)
   # entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    #protecting edit
    if topic.owner !=request.user:
        raise Http404
    
    if request.method !='POST':
        #initial request,pre-fill form with the current entry
        form=EntryForm(instance=entry)
    else:
        #POST data submitted ,process data
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic',topic_id=topic.id)
    
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'entry.html',context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Optional: Ensure only the owner can delete
    if topic.owner != request.user:
        return redirect('logs:topics')  # Redirect unauthorized users

    topic.delete()
    return redirect('logs:topics')  # Redirect after deleting

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic  # Store topic before deleting entry

    # Ensure only the owner can delete
    if topic.owner != request.user:
        return redirect('logs:topics')

    entry.delete()

    # Redirect to topics if no entries remain
    if not topic.entry_set.exists():
        return redirect('logs:topics')

    return redirect('logs:topic', topic_id=topic.id)


