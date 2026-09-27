resource "random_pet" "serveur" {
  length = 2

}

resource "local_file" "fiche" {
  filename = "${path.module}/fiche-serveur.txt"
  content  = "Serveur ${random_pet.serveur.id} créé par ${var.prenom}\n"

}