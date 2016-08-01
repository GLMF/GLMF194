#include <gtk/gtk.h>
#include <glib/gi18n.h>

// Voir a la fin du fichier
void addCSS();
GtkWidget* findChildByName(GtkWidget *container,const gchar *name);

#define PACKAGE "cb-login"
#define LOCALE_DIR "/usr/share/locale"

///////////////////////////////////////////////////////////////////////////////
// Prise en compte des fichiers de traduction
///////////////////////////////////////////////////////////////////////////////
void addInternationalisation() {
  bindtextdomain(PACKAGE,LOCALE_DIR);
  bind_textdomain_codeset(PACKAGE,"UTF-8");
  textdomain(PACKAGE);
}
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
    printf("User: %s\n",u);
    printf("Pass: %s\n",p);
  }
}
///////////////////////////////////////////////////////////////////////////////
// Creation de la fenetre et de son contenu
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication *app,gpointer data) {
  addCSS();
  GtkWidget *window=gtk_application_window_new(app);
  gtk_window_set_title(GTK_WINDOW(window),"Application GTK+3 v6");
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
  GtkWidget *label_user=gtk_label_new(_("UserName"));
  gtk_grid_attach(GTK_GRID(grid),label_user,col,row,1,1);
  col++;
  GtkWidget *entry_user=gtk_entry_new();
  gtk_widget_set_name(entry_user,"user");
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_user),_("UserName"));
  gtk_grid_attach(GTK_GRID(grid),entry_user,col,row,1,1);
  col=0;row++;
  GtkWidget *label_pass=gtk_label_new(_("Password"));
  gtk_grid_attach(GTK_GRID(grid),label_pass,col,row,1,1);
  col++;
  GtkWidget *entry_pass=gtk_entry_new();
  gtk_widget_set_name(entry_pass,"pass");
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_pass),_("Password"));
  gtk_entry_set_visibility(GTK_ENTRY(entry_pass),FALSE);
  gtk_grid_attach(GTK_GRID(grid),entry_pass,col,row,1,1);
  col=0;row++;
  GtkWidget *btn=gtk_button_new_with_label(_("Authentication"));
  gtk_grid_attach(GTK_GRID(grid),btn,col,row,2,1);
  g_signal_connect(btn,"clicked",G_CALLBACK(auth),window);

  gtk_widget_show_all(window);
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  addInternationalisation();
  GtkApplication *app=gtk_application_new("fr.iutbeziers.gtk3-06",
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
///////////////////////////////////////////////////////////////////////////////
// Ajout de la mise en forme CSS
///////////////////////////////////////////////////////////////////////////////
void addCSS() {
  GtkCssProvider *provider=gtk_css_provider_new();
  GdkDisplay *display=gdk_display_get_default();
  GdkScreen *screen=gdk_display_get_default_screen(display);
  gtk_style_context_add_provider_for_screen(screen,
                                            GTK_STYLE_PROVIDER(provider),
                                            GTK_STYLE_PROVIDER_PRIORITY_USER);
  GError *error=NULL;
  gtk_css_provider_load_from_path(provider,"style.css",&error);
  if (error!=NULL) {
    fprintf(stderr,"Unable to load CSS file: %s !\n",error->message);
    g_error_free(error);
  }
  g_object_unref(provider);
}
