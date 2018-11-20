from django.shortcuts import render
import pulp

def homeView(requests):
	return render(requests,'index.html',{})

def simplex_input(requests):
	return render(requests,'simplex_input.html',{})


def simplex_calculate(requests):
	if(requests.method=='POST'):
		no_vars = requests.POST['no_var']
		var_names = requests.POST['var_names']
		var_bounds = requests.POST['var_bounds']
		obj_fn = requests.POST['obj_fn']
		constraints = requests.POST['constraints']
		p_type = requests.POST['p_type']
		context = {}

		if p_type=='maximize':
			my_lp_problem = pulp.LpProblem("Given LP Problem", pulp.LpMaximize)
		else:
			my_lp_problem = pulp.LpProblem("Given LP Problem", pulp.LpMinimize)

		try:
			var_names = var_names.split(',')
			var_bounds = var_bounds.split(',')
			constraints = constraints.split(',')

			ref_var_names = []

			for var_name,var_bound in zip(var_names,var_bounds):
				# must convert var_bound to int
				ref_var_names.append(pulp.LpVariable(var_name, lowBound=int(var_bound), cat='Continuous')) 

			for i in range(len(var_names)):
				obj_fn = obj_fn.replace(var_names[i],'ref_var_names['+str(i)+']')


			# Objective function

			my_lp_problem += eval(obj_fn), "Z"

			for constraint in constraints:
				for i in range(len(var_names)):
					constraint = constraint.replace(var_names[i],'ref_var_names['+str(i)+']')
				my_lp_problem += eval(constraint)	
							
			problem = str(my_lp_problem).split('\n')

			context['problem'] = problem

			my_lp_problem.solve()
			context['status'] = str(pulp.LpStatus[my_lp_problem.status])

			solution = []
			for variable in my_lp_problem.variables():
				solution.append([variable.name, variable.varValue])

			context['solution'] = solution
			context['optimalVal'] = str(pulp.value(my_lp_problem.objective))
			
			return render(requests,'simplex_output.html',context)

		except Exception as e:
			context = {'error':'There is a problem with your input , Please correct it and try again'}
			return render(requests,'simplex_input.html',context)
			
		else:
			pass
		finally:
			pass

		
	else:
		return render(requests,'index.html',{})

