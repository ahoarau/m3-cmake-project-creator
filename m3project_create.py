#!/usr/bin/python

import gtk, gobject
import os, pwd
from datetime import datetime
import re

class FileGenerator():
    def __init__(self,classname,root_path,project_name,comp_name,author=''):
        self.author = author
        assert os.path.isdir(root_path)
        assert len(classname)>0
        self.classname = classname
        self.root_path = self.__process_path(root_path) #mekabot
        self.filename = [self.__get_filename_from_class(c) for c in self.classname]
        self.project_name = project_name
        self.comp_name = comp_name
        
        self.src_dir = '/src'
        self.inc_dir = '/include'
        self.proto_dir = '/proto'
        self.py_dir = '/python'
        self.factory_filename = 'factory_proxy.cpp'
        self.pretty_print()
    def get_component_name(self):
        return self.comp_name
    def __get_filename_from_class(self,classname):
        l = [e.lower() for e in re.findall('[A-Z][^A-Z]*',classname)] #Splits regarding to upper cases
        f = ''
        i = 0
        for i in xrange(len(l)):
            if len(l[i])==1 or i==0:
                f=f+l[i]
            else:
                f=f+'_'+l[i]
        return f
    def get_project_name(self):
        return self.project_name
    def get_factory_filename(self):
        return self.factory_filename
    def get_filename(self):
        return self.filename
    
    def pretty_print(self):
        print 'Root Folder:',self.root_path
        print 'Project name:',self.project_name
        print 'Component name:',self.comp_name
        for f,c in zip(self.get_filename(),self.get_class_name()):
            print 'For filename:',f
            print '- ClassName:',c
            print '- src file:',self.get_source_filepath_local(f)
            print '- hdr file:',self.get_header_filepath_local(f)
            print '- proto file:',self.get_proto_filepath_local(f)
            print '- protobuf file:',self.get_pb_h_filepath_local(f)
            print '- python file:',self.get_python_filepath_local(f)
    def get_author(self):
        return self.author
    def __get_sub_path(self):
        return self.project_name +'/' + self.comp_name
    
    def __process_path(self,path):
        if not path[0]=='/':
            path = '/'+path
        if path[-1]=='/':
            return path[:-1]
        return path
    
    def get_project_path(self):
        return self.root_path+'/'+self.project_name
    
    def get_source_filename(self,f):
        return f+'.cpp'
    
    def get_header_filename(self,f):
        return f+'.h'
    
    def get_proto_filename(self,f):
        return f+'.proto'
    
    def get_python_filename(self,f):
        return f+'.py'
    
    def get_pb_h_filename(self,f):
        return f+'.pb.h'
    
    def get_factory_filepath(self):
        return self.get_source_path()+'/'+self.get_factory_filename()
    def get_source_filepath(self,f):
        return self.get_source_path()+'/'+self.get_source_filename(f)
    def get_source_filepath_local(self,f):
        return self.__get_sub_path()+'/'+self.get_source_filename(f)
    
    def get_header_filepath(self,f):
        return self.get_header_path()+'/'+self.get_header_filename(f)
    def get_header_filepath_local(self,f):
        return self.__get_sub_path()+'/'+self.get_header_filename(f)
    
    def get_proto_filepath(self,f):
        return self.get_proto_path()+'/'+self.get_proto_filename(f)
    def get_proto_filepath_local(self,f):
        return self.__get_sub_path()+'/'+self.get_proto_filename(f)
    
    def get_python_filepath(self,f):
        return self.get_python_path()+'/'+self.get_python_filename(f)
    def get_python_filepath_local(self,f):
        return self.__get_sub_path()+'/'+self.get_python_filename(f)
    
    
    def get_pb_h_filepath(self,f):
        return self.get_header_path()+'/'+self.get_pb_h_filename(f)
    def get_pb_h_filepath_local(self,f):
        return self.__get_sub_path()+'/'+self.get_pb_h_filename(f)
    
    def get_proto_path(self):
        return self.get_project_path()+self.proto_dir+'/'+self.__get_sub_path()

    def get_source_path(self):
        return self.get_project_path()+self.src_dir+'/'+self.__get_sub_path()

    
    def get_header_path(self):
        return self.get_project_path()+self.inc_dir+'/'+self.__get_sub_path()

    
    def get_python_path(self):
        return self.get_project_path()+self.py_dir+'/'+self.__get_sub_path()

    def get_class_name(self):
        return self.classname

    ## The Writing fonctions
    def __create_dir_structure(self):
        self.__safe_makedirs(self.get_project_path())
        self.__safe_makedirs(self.get_header_path())
        self.__safe_makedirs(self.get_source_path())
        self.__safe_makedirs(self.get_proto_path())
        self.__safe_makedirs(self.get_python_path())
        
    def __safe_makedirs(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)
            return True
        else:
            print "Folder",path,"already exists, skipping creation."
            return False
            
    def __safe_createfile(self,filepath,*args):
        if not os.path.exists(filepath):
            print 'Creating file:',filepath
            return open(filepath,'w')
        else:
            print "File",filepath,"already exists, skipping creation."
            return None
    def write_files(self):
        self.__create_dir_structure()
        self.__generate_cmakefiles()
        self.__generate_factory_proxy_file()
        self.__generate_protofiles()
        self.__generate_component_files()
    def __is_str_in_file(self,str,filepath):
        with open(filepath,'r') as f:
                for line in f:
                    if line.find(str)>=0:
                        return True
        return False

    def __generate_cmakefiles(self):
        match_elem=[]
        match_elem.append(['__PROJECT_CREATOR_COMP_NAME__',self.get_component_name()])
        match_elem.append(['__PROJECT_CREATOR_PROJECT_NAME__',self.get_project_name()])
        match_elem.append(['__PROJECT_CREATOR_PROJECT_NAME_UPPER__',self.get_project_name().upper()])
        match_elem.append(['__PROJECT_CREATOR_PROTO_DIR__',self.get_proto_path()])
        match_elem.append(['__PROJECT_CREATOR_PYTHON_DIR__',self.get_python_path()])

        self.__replace_in_file('templates/CMakeLists_top.txt.in', self.get_project_path()+'/'+'CMakeLists.txt', match_elem,overwrite=False)
        
        self.__replace_in_file('templates/CMakeLists_src.txt.in', self.get_source_path()+'/'+'CMakeLists.txt', match_elem,overwrite=True)
        
        cmakelists_sub_filepath = self.get_project_path()+self.__process_path(self.src_dir)+'/'+self.get_project_name()+'/'+'CMakeLists.txt'
        if os.path.isfile(cmakelists_sub_filepath):
            # First look if already there
            if self.__is_str_in_file('add_subdirectory('+self.get_component_name()+')',cmakelists_sub_filepath):
                print 'add_subdirectory('+self.get_component_name()+') already in ',cmakelists_sub_filepath+',skipping edition.'
            else: # Add at the end                
                with open(cmakelists_sub_filepath, "a") as f:
                    f.write(
    """
    add_directory("""+self.get_component_name()+""")
    """)
        else:
            self.__replace_in_file('templates/CMakeLists_sub.txt.in', cmakelists_sub_filepath, match_elem,overwrite=False)
            
    def __replace_in_file(self,filepath_in,filepath_out,matching_element,overwrite=False):
        if overwrite or not os.path.isfile(filepath_out): 
            with open(filepath_out, 'w') as fout:
                with open(filepath_in, 'r') as fin:
                    for line in fin:
                        for s in matching_element:
                            if line.find(s[0])>=0:
                                line = line.replace(s[0],s[1])
                        fout.write(line)
        else:
            print 'File',filepath_out,'already exists, skipping creation.'
            
    def __generate_factory_proxy_file(self):
        project_name = self.get_project_name()
        comp_name = self.get_component_name()
        
        project_name_upper = self.get_project_name().upper()
        
        fwrite = open(self.get_factory_filepath(), 'w')
        print 'Creating file:',self.get_factory_filepath()
        header = """
/* 
MEKA CONFIDENTIAL

Copyright 2011
Meka Robotics LLC
All Rights Reserved.

NOTICE:  All information contained herein is, and remains
the property of Meka Robotics LLC. The intellectual and 
technical concepts contained herein are proprietary to 
Meka Robotics LLC and may be covered by U.S. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material
is strictly forbidden unless prior written permission is obtained
from Meka Robotics LLC.
*/
#include <stdio.h>
#include <m3rt/base/component.h>
"""
        extern_open = """
extern "C" 
{
"""
        class_open = """
    class M3FactoryProxy 
    { 
    public:
        M3FactoryProxy()
        {
"""
        defines = ""
        includes = ""
        creators = ""
        deletors = ""
        registers = ""
        for name,f in zip(self.get_class_name(),self.get_filename()):
            defines = defines + "    #define " + project_name_upper + "_" + f.upper() + "_NAME" + " \"" + f + "\"\n"
            creators = creators + "    m3rt::M3Component* create_" + f.lower() + "(){return new " + project_name + "::" + name + ";}\n"
            deletors = deletors + "    void destroy_" + f.lower() + "(m3rt::M3Component* c) {delete c;}\n"
            registers = registers + "            m3rt::creator_factory[" + project_name_upper + "_" + f.upper() + "_NAME" + "] = create_" + f.lower() + ";\n"
            registers = registers + "            m3rt::destroy_factory[" + project_name_upper + "_" + f.upper() + "_NAME" + "] = destroy_" + f.lower() + ";\n"
            includes = includes + "#include <"+self.get_header_filepath_local(f)+">\n"

        class_close = """
        }
    };

    ///////////////////////////////////////////////////////
    // The library's one instance of the proxy
    M3FactoryProxy proxy;
}
"""
        content = header + includes + extern_open + defines + '\n' + creators + '\n' + deletors + class_open + registers + class_close
        if fwrite:
            fwrite.write(content)
            fwrite.close()



    def __get_gpl_header(self, author, description="Part of the M3 realtime control system by Meka Robotics LLC.", year=datetime.now().year):
        header = "/**\n"
        header = header + " * " + description + "\n" + " * Copyright (C) Meka Robotics LLC %d"%year
        header = header + "  " + author + "\n"
        header = header + """ *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
"""
        return header

    def __generate_component_header(self,class_name,f):
        project_name = self.get_project_name()
        comp_name =self.get_component_name()
        
        ifdefs = "#ifndef " + project_name.upper() + "_" + f.upper() + "_H\n"
        ifdefs = ifdefs + "#define " + project_name.upper() + "_" + f.upper() + "_H\n"

        includes = """
#include <m3rt/base/component.h>
#include <google/protobuf/message.h>
"""
        includes = includes + "#include \"" +self.get_pb_h_filepath_local(f)+"\"\n"
        content = self.__get_gpl_header(self.get_author()) + ifdefs + includes
        content = content + "\nnamespace " + project_name
        content = content + """
{
using namespace std;
using namespace m3;

class """
        content = content +  class_name + " : public m3rt::M3Component" + """
{
        public:
"""         
        content = content + "                " + class_name + "(): m3rt::M3Component() {}\n"
        content = content + "                virtual ~" + class_name + "(){}\n"
        content = content + """
                google::protobuf::Message * GetCommand(){return &command;}
                google::protobuf::Message * GetStatus(){return &status;}
                google::protobuf::Message * GetParam(){return &param;}

        protected:
                bool ReadConfig(const char * filename);
                void Startup();
                void Shutdown();
                bool LinkDependentComponents();
                void StepStatus();
                void StepCommand();
"""
        content = content + "                " +  class_name + " status;\n" + "                " +  class_name + " command;\n" + "                " + class_name + " param;\n" + "                " + "M3BaseStatus * GetBaseStatus(){return status.mutable_base();}\n"
        content = content + """
        private:
                string dependency_name;
                M3DependencyComponent * dep;
};
}
#endif
"""
        return content

    def __generate_component_body(self, class_name,f):
        project_name = self.get_project_name()
        comp_name =self.get_component_name()
        
        includes = "#include \"" +self.get_header_filepath_local(f)+"\"\n"
        includes = includes + """
#include <m3rt/base/m3rt_def.h>
#include <m3rt/base/component_factory.h> 

"""
        content = includes
        content = content + "namespace " + project_name + " {"
        content = content +  """
using namespace m3rt;
using namespace std;

"""
        content = self.__get_gpl_header(self.get_author()) + content + "bool " + class_name + """::ReadConfig(const char * filename)
{
        YAML::Node doc;
        GetYamlDoc(filename, doc);

        if (!M3Component::ReadConfig(filename))
                return false;
        
        doc["foo_name"] >> foo_name;
        double val;
        doc["param"]["gain"] >> val;
        param.set_gain(val);

        return true;
}

"""
        content = content + "bool " + class_name + """::LinkDependentComponents()
{
        foo=(M3Foo*) factory->GetComponent(foo_name);
        if (foo==NULL)
        {
                M3_INFO("M3Foo component %s not found for component %s\\n",foo_name.c_str(),GetName().c_str());
                return false;
        }
        return true;
}

"""
        content = content + "void " + class_name + """::Startup()
{
        if (foo==NULL)
                SetStateError();
        else
                SetStateSafeOp();
}

"""
        content = content + "void " + class_name + "Shutdown(){}"
        content = content + "void " + class_name + """StepStatus()
{
        status.set_sensor(foo->GetSensorVal()*param.gain()); 
}

"""
        content = content + "void " + class_name + """::StepCommand()
{
        if (command.enable())
        {
                foo->EnableControler();
        }

}

}"""
        return content

    def __generate_protofiles(self):
        
        for f,c in zip(self.get_filename(),self.get_class_name()):
            match_elem = []
            match_elem.append(['__PROJECT_CREATOR_AUTHOR__',self.get_author()])
            match_elem.append(['__PROJECT_CREATOR_CLASS_NAME__',c])
            self.__replace_in_file('example.proto', self.get_proto_filepath(f), match_elem, overwrite=True)
            
            
    def __generate_component_files(self):
        project_dir = self.get_project_path()
        comp_name = self.get_component_name()
        
        for name,f in zip(self.get_class_name(),self.get_filename()):
            # Header
            fwrite = self.__safe_createfile(self.get_header_filepath(f), 'w')
            header_file = self.__generate_component_header(name,f)
            if fwrite:
                fwrite.write(header_file)
                fwrite.close()
            # Body:
            fwrite = self.__safe_createfile(self.get_source_filepath(f), 'w')
            body_file = self.__generate_component_body(name,f)
            if fwrite:
                fwrite.write(body_file)
                fwrite.close()

class M3ComponentAssistant(gtk.Assistant):
    def __init__(self):
        gtk.Assistant.__init__(self)
        self.set_title("M3 CMake Project Creator")
        self.connect('prepare', self.__prepare_page_cb)
        self.scrolled_window = None

        self.connect('close', self.cb_close)        
        
        self.connect("cancel", self.cb_close)
        
        self.connect("apply", self.cb_apply)
      
        self.component_count = 1

        self.__add_page_intro()
        
        self.__add_page_component()

        self.__add_page_confirm()
        
        self.set_default_size(400, 400)

        self.show()

    def __prepare_page_cb(self, widget, page):
        if page == self.page_confirm:
            if self.scrolled_window != None:
                self.page_confirm.remove(self.scrolled_window)
            treeview_confirm = self.__create_component_treeview()
            self.scrolled_window = gtk.ScrolledWindow()
            self.scrolled_window.add_with_viewport(treeview_confirm)
            self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            self.page_confirm.pack_start(self.scrolled_window, expand=True)
            self.page_confirm.show_all()

    def __get_username(self):
       comment = pwd.getpwuid(os.getuid())[4]
       name = comment.split(',')[0]
       if name == "":
           return pwd.getpwuid(os.getuid())[0]

       return name

    def __add_page_intro(self):
     # First page                  
        vbox = gtk.VBox(False, 4)
        vbox.set_border_width(4)
        
        label = gtk.Label("\nThis assistant will help you generate a new M3 project using the new CMake integration.\nIn the following page, you will get to specify the components that you need to create.\n")   
        label.set_line_wrap(True)
        vbox.pack_start(label, True, True, 0)
        
        table = gtk.Table(4, 2, True)
        table.set_row_spacings(4)
        table.set_col_spacings(4)
        
        # Author
        label = gtk.Label("Author :")
        table.attach(label, 0, 1, 0, 1)
        self.author_entry = gtk.Entry()
        self.author_entry.set_text(self.__get_username())
        table.attach(self.author_entry, 1, 2, 0, 1)
        
        # Project name # should be m3ens, m3uta etc
        label = gtk.Label("Project Name :")
        table.attach(label, 0, 1, 1, 2)
        self.entry = gtk.Entry()
        self.entry.set_text("m3ens")
        table.attach(self.entry, 1, 2, 1, 2)
        self.entry.connect('changed', self.changed_comp_name_cb)
        
        # Component name 
        label = gtk.Label("Components Name :")
        table.attach(label, 0, 1, 2, 3)
        self.entry_comp_folder = gtk.Entry()
        self.entry_comp_folder.set_text("mycomponent")
        table.attach(self.entry_comp_folder, 1, 2, 2, 3)
        self.entry_comp_folder.connect('changed', self.changed_comp_name_cb)
        
        vbox.pack_start(table, True, False, 0)

        # File chooser
        table.attach(gtk.Label("Root folder :"), 0, 1, 3, 4)
        table.attach(gtk.Label("(ex: mekabot)"), 0, 3, 3, 4)
        self.file_chooser = gtk.FileChooserButton('Select a folder')
        self.file_chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        table.attach(self.file_chooser, 1, 2, 3, 4)
        vbox.show_all()

        self.append_page(vbox)
        self.set_page_title(vbox, 'M3 CMake Project Creator')
        self.set_page_type(vbox, gtk.ASSISTANT_PAGE_CONTENT)
        
        self.set_page_complete(vbox, True)
    def changed_comp_name_cb(self,entry):
        entry_text = entry.get_text()
        entry_text = entry_text.replace(' ', '')
        entry_text = entry_text.strip()
        entry_text = entry_text.lower()
        entry.set_text(entry_text)
        return

        
    def edited_cb(self, cell, path, new_text, model ):
        entry_text = model[path][0]
        new_text = new_text[0].upper() + new_text[1:]
        new_text = new_text.replace(' ', '')
        new_text = new_text.strip()
        model[path][0] = new_text
        return

    def prio_edited_cb(self, renderer, path, new_text):
        itr = self.store.get_iter( path )
        self.store.set_value( itr, 1, new_text )

    def toggled_cb(self, cell, path_str, model):
        # get toggled iter
        iter = model.get_iter_from_string(path_str)
        toggle_item = model.get_value(iter, 2)
  
        # do something with the value
        toggle_item = not toggle_item
  
        # set new value
        model.set(iter, 2, toggle_item)

    def add_button_cb(self, widget):
        self.store.append(('Controller%d'%self.component_count, 'ROBOT_PRIORITY', False))
        self.component_count += 1
        
    def delete_button_cb(self, widget):
        path, column = self.treeview.get_cursor()
        iter = self.store.get_iter(path)
        self.store.remove(iter)

    def __add_page_component(self):
        vbox = gtk.VBox(False, 4)
        vbox.set_border_width(4)

        # Create buttons
        hbbox = gtk.HButtonBox()
        hbbox.set_layout(gtk.BUTTONBOX_END)
        hbbox.set_spacing(4)

        add_button = gtk.Button(stock=gtk.STOCK_ADD)
        add_button.connect('clicked', self.add_button_cb)
        delete_button = gtk.Button(stock=gtk.STOCK_DELETE)
        delete_button.connect('clicked', self.delete_button_cb)

        hbbox.add(add_button)
        hbbox.add(delete_button)

        vbox.pack_end(hbbox, False, False, 0)

        # Create model for combo
        self.prio_combo_model = gtk.ListStore(gobject.TYPE_STRING)
        self.prio_combo_model.append(["MAX_PRIORITY"])
        self.prio_combo_model.append(["EC_PRIORITY"])
        self.prio_combo_model.append(["CALIB_PRIORITY"])
        self.prio_combo_model.append(["JOINT_PRIORITY"])
        self.prio_combo_model.append(["DYNAMATICS_PRIORITY"])
        self.prio_combo_model.append(["ROBOT_PRIORITY"])
        self.prio_combo_model.append(["ROBOT_CTRL_PRIORITY"])
        self.prio_combo_model.append(["ARM_HEAD_DYNAMATICS_PRIORITY"])

        # Create the model
        self.store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        self.store.append(('ControllerExample', 'ROBOT_CTRL_PRIORITY', False))

        # Create treeview
        self.treeview = gtk.TreeView(self.store)

        # Create cell renderers
        self.cellrenderer_name = gtk.CellRendererText()
        self.cellrenderer_name.set_property('editable', True)
        self.cellrenderer_name.connect('edited', self.edited_cb,self.store)
        
        self.cellrenderer_prio = gtk.CellRendererCombo()
        self.cellrenderer_prio.set_property("model", self.prio_combo_model)
        self.cellrenderer_prio.set_property('has-entry', False)
        self.cellrenderer_prio.set_property('text-column', 0)
        self.cellrenderer_prio.set_property('editable', True)
        self.cellrenderer_prio.connect('edited', self.prio_edited_cb)

        self.cellrenderer_ec = gtk.CellRendererToggle()
        self.cellrenderer_ec.set_property('activatable', True)
        self.cellrenderer_ec.connect('toggled', self.toggled_cb, self.store)

        # Create columns
        self.column_name = gtk.TreeViewColumn("Name", self.cellrenderer_name, text=0)
        self.column_name.set_resizable(True)
        self.column_name.set_expand(True)

        self.column_prio = gtk.TreeViewColumn("Priority", self.cellrenderer_prio)
        self.column_prio.set_resizable(True)
        self.column_prio.set_expand(True)
        self.column_prio.add_attribute(self.cellrenderer_prio, "text", 1)

        self.column_ec = gtk.TreeViewColumn("EC Attached", self.cellrenderer_ec)
        self.column_ec.add_attribute(self.cellrenderer_ec, "active", 2)

        self.treeview.append_column(self.column_name)
        self.treeview.append_column(self.column_prio)
        self.treeview.append_column(self.column_ec)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add_with_viewport(self.treeview)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)
        vbox.show_all()

        self.append_page(vbox)
        self.set_page_title(vbox, 'Your Components Class Name (Inherit from M3Component)')
        self.set_page_type(vbox, gtk.ASSISTANT_PAGE_CONTENT)

        self.set_page_complete(vbox, True)

    def __get_project_name(self):
        return self.entry.get_text()

    def __get_components_info(self):
        return [(row[0], row[1], row[2]) for row in self.store]

    def __get_components_class_name(self):
        names = []
        for row in self.store:
            name = row[0]
            names.append(name)
            if row[2] == True:
                names.append(name + "Ec")
        return names

    def __get_components_name(self):
        names = []
        for row in self.store:
            name = row[0]
            names.append(name)
            if row[2] == True:
                names.append(name + "Ec")
        return names


    def __get_comp_folder_name(self):
        return self.entry_comp_folder.get_text()
    def __get_root_dir(self):
        return self.file_chooser.get_filename()




    def __add_sub_com(self,store,top):
        pname = store.append(top,[self.__get_project_name()+'/'])
        pcomp = store.append(pname,[self.__get_comp_folder_name()+'/'])
        return pcomp
    def __create_component_treeview(self):
        
        root_dir = self.__get_root_dir()
        project_name = self.__get_project_name()
        comp_name = self.__get_comp_folder_name()
        
        self.fgen=FileGenerator(self.__get_components_class_name(),root_dir,project_name,comp_name,self.__get_username())
        project_dir = self.fgen.get_project_path()

        store = gtk.TreeStore(gobject.TYPE_STRING)
        
        iter_root = store.append(None, [project_dir + "/"])
        iter_src = store.append(iter_root, [self.fgen.src_dir+'/'])
        iter_inc = store.append(iter_root, [self.fgen.inc_dir+'/'])
        iter_py = store.append(iter_root, [self.fgen.py_dir+'/'])
        iter_proto = store.append(iter_root, [self.fgen.proto_dir+'/'])
        
        
        iter_components = self.__add_sub_com(store, iter_src)
        store.append(iter_components, [self.fgen.get_factory_filename()])
        for f in self.fgen.get_filename():
            store.append(iter_components, [self.fgen.get_source_filename(f)])
            
        iter_components = self.__add_sub_com(store, iter_inc)
        for f in self.fgen.get_filename():
            store.append(iter_components, [self.fgen.get_header_filename(f)])
        
        iter_components = self.__add_sub_com(store, iter_proto)
        for f in self.fgen.get_filename():
            store.append(iter_components, [self.fgen.get_proto_filename(f)])
            
        iter_components = self.__add_sub_com(store, iter_py)
        for f in self.fgen.get_filename():
            store.append(iter_components, [self.fgen.get_python_filename(f)])

        # Create treeview
        treeview = gtk.TreeView(store)
        cellrenderer_name = gtk.CellRendererText()
        column_name = gtk.TreeViewColumn("Project", cellrenderer_name, text=0)
        treeview.append_column(column_name)
        treeview.expand_all()

        return treeview

    def __add_page_confirm(self):
        self.page_confirm = gtk.VBox(False, 4)
        
        label = gtk.Label()
        label.set_markup("The following project will be generated.")
        label.set_line_wrap(True)
        self.page_confirm.pack_end(label, expand=False)                             
        self.page_confirm.show_all();

        self.append_page(self.page_confirm)
        self.set_page_title(self.page_confirm, "Confirm and Create CMake Project")
        self.set_page_type(self.page_confirm, gtk.ASSISTANT_PAGE_CONFIRM)        
        self.set_page_complete(self.page_confirm, True)        

    def cb_close(self, widget):
        gtk.main_quit()
        
    def cb_apply(self, widget):
        self.fgen.write_files()
        return
        
if __name__ == '__main__':
    win = M3ComponentAssistant()
    win.show()
    gtk.main()
