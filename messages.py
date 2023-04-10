#-------------------------------------------------------------------------------
# Name:			messages.py
# Purpose:		"gncdisplay" app
#				email messages to be sent by app
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

reset_password = """(Ré)initialisation de ton mot de passe
Bonjour {0},

Tu as demandé la création ou la réinitialisation de ton mot de passe pour accéder aux comptes des Minimes.
Pour choisir ton nouveau mot de passe suis ce lien:
{1}

Ce lien est valable 30 minutes.

Bien cordialement,
Alain Goyé
"""

# ###################### logging and registering participants
connexion_failed =	"La connexion a échoué; veuillez vérifier vos identifiants"
logout_ok =			"Vous avez bien été déconnecté"

# ###################### resetting password
reset_mail_sent =	"Si vous avez fourni une adresse mail valide, un message vous a été envoyé. Veuillez consulter votre messagerie"
error_occured =		"Une erreur s'est produite"
invalid_link = 		"Une erreur s'est produite. Le lien utilisé est invalide"
reset_lnk_timeout =	"Le lien de réinitialisation du mot de passe a expiré"
pwd_not_recorded = 	"Une erreur s'est produite, le mot de passe n'a pas été enregistré"
pwd_reset_timeout = "Le délai de réinitialisation du mot de passe a expiré"
invalid_pwd = 		"Le mot de passe fourni n'est pas valide. Veuillez réessayer"
pwd_recorded = 		"Votre nouveau mot de passe a été enregistré avec succès"