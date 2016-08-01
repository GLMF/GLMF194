#include <gtk/gtk.h>

int nb=0; // Compteur du nombre de clics

///////////////////////////////////////////////////////////////////////////////
// Fonction executee a chaque clic sur le bouton
///////////////////////////////////////////////////////////////////////////////
static void click(GtkWidget *b,gpointer data) {
  char msg[10];
  snprintf(msg,sizeof(msg),"Click: %d",nb++);
  gtk_button_set_label(GTK_BUTTON(b),msg);
  // Utilise le parametre indique ligne 55
  if (data!=NULL) {
    GtkWindow *window=(GtkWindow *)data;
    gtk_window_set_title(window,msg);
  }
}
///////////////////////////////////////////////////////////////////////////////
// Creation de la fenetre et de son contenu
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication *app,gpointer data) {
  GtkWidget *window=gtk_application_window_new(app);
  gtk_window_set_title(GTK_WINDOW(window),"Application GTK+3 v3");
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
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_user),"UserName");
  gtk_grid_attach(GTK_GRID(grid),entry_user,col,row,1,1);
  col=0;row++;
  GtkWidget *label_pass=gtk_label_new("Password");
  gtk_grid_attach(GTK_GRID(grid),label_pass,col,row,1,1);
  col++;
  GtkWidget *entry_pass=gtk_entry_new();
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_pass),"Password");
  gtk_entry_set_visibility(GTK_ENTRY(entry_pass),FALSE);
  gtk_grid_attach(GTK_GRID(grid),entry_pass,col,row,1,1);
  col=0;row++;
  GtkWidget *btn=gtk_button_new_with_label("Authentication");
  gtk_grid_attach(GTK_GRID(grid),btn,col,row,2,1);
  g_signal_connect(btn,"clicked",G_CALLBACK(click),NULL);
  //g_signal_connect(btn,"clicked",G_CALLBACK(click),window);

  gtk_widget_show_all(window);
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  GtkApplication *app=gtk_application_new("fr.iutbeziers.gtk3-03",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
