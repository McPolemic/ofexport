import os
import codecs
import getopt
import sys
from treemodel import traverse_list
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from visitors import FolderNameFilterVisitor, ProjectNameFilterVisitor, ProjectFlaggedFilterVisitor, ProjectDueFilterVisitor, ProjectStartFilterVisitor, ContextNameFilterVisitor, TaskDueFilterVisitor, TaskNameFilterVisitor, TaskStartFilterVisitor, TaskCompletionFilterVisitor, ProjectCompletionFilterVisitor, TaskCompletionSortingVisitor, TaskFlaggedFilterVisitor, PruningFilterVisitor, FlatteningVisitor

VERSION = "1.0.0 (2013-04-09)" 
     
def print_structure (visitor, root_projects_and_folders, root_contexts, project_mode):
    if project_mode:
        traverse_list (visitor, root_projects_and_folders)
    else:
        traverse_list (visitor, root_contexts)

class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def tags (self, completed):
        if completed != None:
            return completed.strftime(" @%Y-%m-%d-%a")
        else:
            return ""
        
def print_help ():
    print 'Version ' + VERSION
    print 
    print 'Usage:'
    print
    print 'ofexport [options...] -o file_name'
    print
    print
    print 'options:'
    print '  -h,-?,--help'
    print '  -C: context mode (as opposed to project mode)'
    print '  -o file_name: the output file name, must end in a recognised suffix - see documentation'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'filters:'
    
    print '  --pi regexp: include projects matching regexp'
    print '  --pe regexp: exclude projects matching regexp'
    
    print '  --pci regexp: include projects with completion matching regexp'
    print '  --pce regexp: exclude projects with completion matching regexp'
    
    print '  --pdi regexp: include projects with due matching regexp'
    print '  --pde regexp: exclude projects with due matching regexp'
    
    print '  --psi regexp: include projects with start matching regexp'
    print '  --pse regexp: exclude projects with start matching regexp'
    
    print '  --pfi: include flagged projects'
    print '  --pfe: exclude flagged projects'
    
    print '  --fi regexp: include folders matching regexp'
    print '  --fe regexp: exclude folders matching regexp'
    
    print '  --ti regexp: include tasks matching regexp'
    print '  --te regexp: exclude tasks matching regexp'
    
    print '  --ci regexp: include contexts matching regexp'
    print '  --ce regexp: exclude contexts matching regexp'
     
    print '  --tci regexp: include tasks with completion matching regexp'
    print '  --tce regexp: exclude tasks with completion matching regexp'
    
    print '  --tsi regexp: include tasks with start matching regexp'
    print '  --tse regexp: exclude tasks with start matching regexp'
    
    print '  --tdi regexp: include tasks with due matching regexp'
    print '  --tde regexp: exclude tasks with due matching regexp'
    
    print '  --tfi: include flagged tasks'
    print '  --tfe: exclude flagged tasks'
    
    print '  --tsc: sort tasks by completion'
    
    print '  -F: flatten project/task structure'
    print '  --prune: prune empty projects or folders'

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
        
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:], 'hFC?o:',
                                                      ['fi=','fe=',
                                                       'ci=','ce=',
                                                       'pi=','pe=',
                                                       'pci=','pce=',
                                                       'psi=','pse=',
                                                       'pdi=','pde=',
                                                       'pfi','pfe',
                                                       'ti=','te=',
                                                       'tci=','tce=',
                                                       'tsi=','tse=',
                                                       'tdi=','tde=',
                                                       'tfi','tfe',
                                                       'tsc',
                                                       'help',
                                                       'open',
                                                       'prune'])
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '-C' == opt:
            project_mode = False
        elif '-o' == opt:
            file_name = arg;
        elif opt in ('-?', '-h', '--help'):
            print_help ()
            sys.exit()
    
    if file_name == None:
            print_help ()
            sys.exit()
    
    dot = file_name.index ('.')
    if dot == -1:
        print 'output file name must have suffix'
        sys.exit()
    
    fmt = file_name[dot+1:]
    
    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    if project_mode:
        items = root_projects_and_folders
    else:
        items = root_contexts
        
    for opt, arg in opts:
        
        # FOLDER
        if '--fi' == opt:
            print 'include folders', arg
            traverse_list (FolderNameFilterVisitor (arg, include=True), items)
        elif '--fe' == opt:
            print 'exclude folders', arg
            traverse_list (FolderNameFilterVisitor (arg, include=False), items)
        
        # PROJECT
        elif '--pi' == opt:
            print 'include project', arg
            traverse_list (ProjectNameFilterVisitor (arg, include=True), items)
        elif '--pe' == opt:
            print 'exclude project', arg
            traverse_list (ProjectNameFilterVisitor (arg, include=False), items)
        elif '--psi' == opt:
            print 'include project start', arg
            traverse_list (ProjectStartFilterVisitor (arg, include=True), items)
        elif '--pse' == opt:
            print 'exclude project start', arg
            traverse_list (ProjectStartFilterVisitor (arg, include=False), items)
        elif '--pdi' == opt:
            print 'include project due', arg
            traverse_list (ProjectDueFilterVisitor (arg, include=True), items)
        elif '--psc' == opt:
            print 'exclude project due', arg
            traverse_list (ProjectDueFilterVisitor (arg, include=False), items)
        elif '--pci' == opt:
            print 'include project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=True), items)
        elif '--pce' == opt:
            print 'exclude project completion', arg
            traverse_list (ProjectCompletionFilterVisitor (arg, include=False), items)
        elif '--pfi' == opt:
            print 'include project completion'
            traverse_list (ProjectFlaggedFilterVisitor (arg, include=True), items)
        elif '--pfe' == opt:
            print 'exclude project completion'
            traverse_list (ProjectFlaggedFilterVisitor (arg, include=False), items)
            
        # CONTEXT
        elif '--ci' == opt:
            print 'include contexts', arg
            traverse_list (ContextNameFilterVisitor (arg, include=True), items)
        elif '--ce' == opt:
            print 'exclude contexts', arg
            traverse_list (ContextNameFilterVisitor (arg, include=False), items)
        
        # TASK
        elif '--ti' == opt:
            print 'include tasks', arg
            traverse_list (TaskNameFilterVisitor (arg, include=True), items)
        elif '--te' == opt:
            print 'exclude tasks', arg
            traverse_list (TaskNameFilterVisitor (arg, include=False), items)
        elif '--tci' == opt:
            print 'include task completion', arg
            traverse_list (TaskCompletionFilterVisitor (arg, include=True), items)
        elif '--tce' == opt:
            print 'exclude task completion', arg
            traverse_list (TaskCompletionFilterVisitor (arg, include=False), items)
        elif '--tsi' == opt:
            print 'include task start', arg
            traverse_list (TaskStartFilterVisitor (arg, include=True), items)
        elif '--tse' == opt:
            print 'exclude task start', arg
            traverse_list (TaskStartFilterVisitor (arg, include=False), items)
        elif '--tdi' == opt:
            print 'include task due', arg
            traverse_list (TaskDueFilterVisitor (arg, include=True), items)
        elif '--tde' == opt:
            print 'exclude task due', arg
            traverse_list (TaskDueFilterVisitor (arg, include=False), items)
        elif '--tfi' == opt:
            print 'include flagged tasks'
            traverse_list (TaskFlaggedFilterVisitor (include=True), items)
        elif '--tfe' == opt:
            print 'exclude flagged tasks'
            traverse_list (TaskFlaggedFilterVisitor (include=False), items)
        elif '--tsc' == opt:
            print 'sort by task completion'
            traverse_list (TaskCompletionSortingVisitor (), items)
        
        # MISC
        elif '--prune' == opt:
            print 'pruning empty folders, projects, contexts'
            traverse_list (PruningFilterVisitor (), items)
        elif '-F' == opt:
            visitor = FlatteningVisitor ()
            traverse_list (visitor, root_projects_and_folders)
            root_projects_and_folders = visitor.projects

    file_name_base = os.environ['HOME']+'/Desktop/'
    date_str = today.strftime (time_fmt)
    
    if fmt == 'txt' or fmt == 'text':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintTextVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # MARKDOWN
    elif fmt == 'md' or fmt == 'markdown':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # FOLDING TEXT
    elif fmt == 'ft' or fmt == 'foldingtext':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
                
    # TASKPAPER            
    elif fmt == 'tp' or fmt == 'taskpaper':
        out=codecs.open(file_name, 'w', 'utf-8')

        print_structure (CustomPrintTaskpaperVisitor (out), root_projects_and_folders, root_contexts, project_mode)
    
    # OPML
    elif fmt == 'opml':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        print >>out, '<opml version="1.0">'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        print_structure (PrintOpmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </body>'
        print >>out, '</opml>'
    
    # Let's try JSON!
    
    # elif fmt =='json':
    #     out=codexs.open(file_name, 'w', 'utf-8')
    #     print >>out, ''
        
        
    # Statusboard HTML
    elif fmt =='html':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '  <table id="projects">'
        
        print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </table>'
        
    # HTML
    # elif fmt == 'html' or fmt == 'htm':
    #     out=codecs.open(file_name, 'w', 'utf-8')
    #     print >>out, '<html>'
    #     print >>out, '  <head>'
    #     print >>out, '    <title>OmniFocus</title>'
    #     print >>out, '  </head>'
    #     print >>out, '  <body>'
    #     
    #     print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
    #     
    #     print >>out, '  </body>'
    #     print >>out, '<html>'
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
