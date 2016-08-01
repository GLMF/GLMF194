#include <gtk/gtk.h>
#include <string.h>

// Voir a la fin du fichier
GtkWidget* findChildByName(GtkWidget *container,const gchar *name);

///////////////////////////////////////////////////////////////////////////////
// Fonction d'authentification
///////////////////////////////////////////////////////////////////////////////
static void auth(GtkWidget *b,gpointer data) {
  GtkWidget *user=NULL;
  GtkWidget *pass=NULL;
  if (data!=NULL) {
    GtkWidget *window=(GtkWidget *)data;
    user=findChildByName(window,"user");
    pass=findChildByName(window,"pass");
  }
  if (user!=NULL&&pass!=NULL) {
    const gchar *u=gtk_entry_get_text(GTK_ENTRY(user));
    const gchar *p=gtk_entry_get_text(GTK_ENTRY(pass));
    //printf("User: %s\n",u);
    //printf("Pass: %s\n",p);
    // C'EST UN EXEMPLE, NE FAITES JAMAIS CE QUI SUIT !!!
    if (strncmp(u,"toto",4)==0 && strncmp(p,"titi",4)==0) {
      printf("Welcome %s !\n",u);
    } else {
      printf("Wrong password !\n");
    }
    gtk_entry_set_text(GTK_ENTRY(pass),"");
  }
}
///////////////////////////////////////////////////////////////////////////////
// Creation de la fenetre et de son contenu
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication *app,gpointer data) {
  GtkWidget *window=gtk_application_window_new(app);
  gtk_window_set_title(GTK_WINDOW(window),"Application GTK+3 v4");
  gtk_window_set_position(GTK_WINDOW(window),GTK_WIN_POS_CENTER);
  gtk_window_set_default_size(GTK_WINDOW(window),400,100);

  gtk_container_set_border_width(GTK_CONTAINER(window),10);

  GtkWidget *grid=gtk_grid_new();
  gtk_container_add(GTK_CONTAINER(window),grid);
  gtk_grid_set_row_spacing(GTK_GRID(grid),2);
  gtk_grid_set_column_spacing(GTK_GRID(grid),5);
  gtk_widget_set_valign(grid,GTK_ALIGN_CENTER);
  gtk_widget_set_halign(grid,GTK_ALIGN_CENTER);

  int col=0,row=0;
  GtkWidget *label_user=gtk_label_new("UserName");
  gtk_grid_attach(GTK_GRID(grid),label_user,col,row,1,1);
  col++;
  GtkWidget *entry_user=gtk_entry_new();
  gtk_widget_set_name(entry_user,"user");
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_user),"UserName");
  gtk_grid_attach(GTK_GRID(grid),entry_user,col,row,1,1);
  col=0;row++;
  GtkWidget *label_pass=gtk_label_new("Password");
  gtk_grid_attach(GTK_GRID(grid),label_pass,col,row,1,1);
  col++;
  GtkWidget *entry_pass=gtk_entry_new();
  gtk_widget_set_name(entry_pass,"pass");
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_pass),"Password");
  gtk_entry_set_visibility(GTK_ENTRY(entry_pass),FALSE);
  gtk_grid_attach(GTK_GRID(grid),entry_pass,col,row,1,1);
  col=0;row++;
  GtkWidget *btn=gtk_button_new_with_label("Authentication");
  gtk_grid_attach(GTK_GRID(grid),btn,col,row,2,1);
  g_signal_connect(btn,"clicked",G_CALLBACK(auth),window);

  gtk_widget_show_all(window);
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  GtkApplication *app=gtk_application_new("fr.iutbeziers.gtk3-04",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
///////////////////////////////////////////////////////////////////////////////
// Recherche recursive d'un nom dans un conteneur
///////////////////////////////////////////////////////////////////////////////
GtkWidget* findChildByName(GtkWidget *container,const gchar *name) {
  if (GTK_IS_WIDGET(container)) {
    const gchar *cName=gtk_widget_get_name(container);
    if (g_strcmp0(cName,name)==0) { // Le nom du conteneur correspond
      return container;
    }
    if (GTK_IS_BIN(container)) { // Conteneur avec un seul enfant
      GtkWidget *child=gtk_bin_get_child(GTK_BIN(container));
      return findChildByName(child,name);
    }
    if (GTK_IS_CONTAINER(container)) { // Recherche dans la liste des enfants
      GList *childs=gtk_container_get_children(GTK_CONTAINER(container));
      GList *item;
      for(item=childs;item!=NULL;item=g_list_next(item)) {
        GtkWidget *widget=findChildByName(item->data,name);
        if (widget!=NULL) {
          g_list_free(childs);
          return widget;
        }
      }
      if (childs!=NULL) g_list_free(childs);
    }
  }
  return NULL;
}
