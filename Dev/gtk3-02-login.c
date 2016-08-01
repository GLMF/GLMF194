#include <gtk/gtk.h>

///////////////////////////////////////////////////////////////////////////////
// Creation de la fenetre et de son contenu
///////////////////////////////////////////////////////////////////////////////
static void startApplication(GtkApplication *app,gpointer data) {
  GtkWidget *window=gtk_application_window_new(app);
  gtk_window_set_title(GTK_WINDOW(window),"Application GTK+3 v2");
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
  //gtk_entry_set_width_chars(GTK_ENTRY(entry_user),25);
  gtk_grid_attach(GTK_GRID(grid),entry_user,col,row,1,1);
  col=0;row++;
  GtkWidget *label_pass=gtk_label_new("Password");
  gtk_grid_attach(GTK_GRID(grid),label_pass,col,row,1,1);
  col++;
  GtkWidget *entry_pass=gtk_entry_new();
  gtk_entry_set_placeholder_text(GTK_ENTRY(entry_pass),"Password");
  //gtk_entry_set_max_length(GTK_ENTRY(entry_pass),8);
  gtk_entry_set_visibility(GTK_ENTRY(entry_pass),FALSE);
  //gtk_entry_set_invisible_char(GTK_ENTRY(entry_pass),42);
  //gtk_entry_set_input_purpose(GTK_ENTRY(entry_pass),
                              //GTK_INPUT_PURPOSE_PASSWORD);
  gtk_grid_attach(GTK_GRID(grid),entry_pass,col,row,1,1);
  col=0;row++;
  GtkWidget *btn=gtk_button_new_with_label("Authentication");
  //gtk_widget_set_hexpand(btn,FALSE);
  //gtk_widget_set_vexpand(btn,FALSE);
  //gtk_widget_set_halign(btn,GTK_ALIGN_CENTER);
  //gtk_widget_set_valign(btn,GTK_ALIGN_CENTER);
  //gtk_widget_set_size_request(btn,220,50);
  gtk_grid_attach(GTK_GRID(grid),btn,col,row,2,1);

  gtk_widget_show_all(window);
}
///////////////////////////////////////////////////////////////////////////////
// Programme principal
///////////////////////////////////////////////////////////////////////////////
int main(int argc,char *argv[]) {
  GtkApplication *app=gtk_application_new("fr.iutbeziers.gtk3-02",
                                          G_APPLICATION_FLAGS_NONE);
  g_signal_connect(app,"activate",G_CALLBACK(startApplication),NULL);
  int status=g_application_run(G_APPLICATION(app),argc,argv);
  g_object_unref(app);
  return status;
}
