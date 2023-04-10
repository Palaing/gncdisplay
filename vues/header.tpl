<!DOCTYPE html>
<html lang="fr">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>{{titre}}</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
	<div class="container opaquebg">
		<div class="row mb-4">
		<div class="col "><h3>{{entity}}</h3></div>
			<div class="col text-decoration-none">
				<div class="float-right">
					<a href="/logout" class="text-secondary"><i class="fa fa-sign-out"></i> déconnexion</a>
					<b>{{user['prenom']}}</b>
				</div>
			</div>
		</div>
		% if get('message'):
		<div class="row mb-4 alert alert-danger justify-content-center" role="alert">
			<div class="col">{{message}}</div>
		</div>
		% end			
		<div class="row mb-4">
			<div class="col text-center"><h3>{{titre}}</h3></div>
		</div>
	</div>
</body>
</html>
