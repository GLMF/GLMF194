#include <gtk/gtk.h>

///////////////////////////////////////////////////////////////////////////////
// Creation de la fenetre et de son contenu
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication *app,gpointer data) {
  GtkWidget *window=gtk_application_window_new(app);
  gtk_window_set_title(GTK_WINDOW(window),"Application GTK+3 v1");
  gtk_window_set_position(GTK_WINDOW(window),GTK_WIN_POS_CENTER);
  gtk_window_set_default_size(GTK_WINDOW(window),400,100);
  gtk_widget_show_all(window);
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  GtkApplication *app=gtk_application_new("fr.iutbeziers.gtk3-01",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
