<div class="container opaquebg">
	<div class="row mb-4">
		<div class="col "><h3>{{entity}}</h3></div>
		<div class="col-6 text-decoration-none">
			<a href="/show" class="text-info"><i class="fa fa-user"></i> mon compte</a> - 
			<a href="/expenses" class="text-info"><i class="fa fa-credit-card"></i> dépenses</a> - 
			<a href="/evolution" class="text-info"><i class="fa fa-line-chart"></i> évolution</a>
			<a href="/balance" class="text-info"><i class="fa fa-balance-scale"></i> soldes</a>
		</div>
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
