# Define global variables that will be used a lot

# Application Info, will be used to clear and write on console through the app
app_name = 'Dominik'
app_version = '1.00'
app_author = 'crn1'
app_separator = '- - - - - - - - - - -'
app_title = f'{app_name} v{app_version} by {app_author}\n{app_separator}'

# These two variables are going to be changed by an app automatically. See chrome_engine.py
# Because we're pulling constantly data from the web while recruiting, we need these two variables to be easy accessable through the app
current_url = ''
current_html = ''

# Because a lot of commands will need input from a user, we need a switch that'll stop the console to be updated while the user's input ends
active_input = False

# All the addresses of various files inside the Obsidian Vault
obsidian_vault_name = "Aparati"
obsidian_vault_path = "C:\\Users\\crn1\\Dropbox\\Aparati\\"

obsidian_interesting_links_path = obsidian_vault_path + "Inkubator\\Interesantni linkovi.md"
obsidian_ideas_path = obsidian_vault_path + "Inkubator\\Misli.md"

obsidian_talents_path = obsidian_vault_path + "CRM\\Talents\\"
obsidian_talent_template_path = obsidian_vault_path + "Templates\\Talent.md"

obsidian_connections_path = obsidian_vault_path + "CRM\\Connections\\"
obsidian_connection_template_path = obsidian_vault_path + "Templates\\Connection.md"

obsidian_companies_path = obsidian_vault_path + "CRM\\Companies\\"
obsidian_company_template_path = obsidian_vault_path + "Templates\\Company.md"

obsidian_schools_path = obsidian_vault_path + "CRM\\Schools\\"
obsidian_school_template_path = obsidian_vault_path + "Templates\\School.md"

obsidian_snoozes_path = obsidian_vault_path + "CRM\\Snoozes\\"
obsidian_snooze_template_path = obsidian_vault_path + "Templates\\Snooze.md"

obsidian_companies_database_path = obsidian_vault_path + "CRM\\Companies Database.xlsx"

# This is a list of all the companiy names that'll be ommited during comparasion. See obsidian_colleagues_and_alumni.py
forbidden_company_names = [
'', #Company name cannot be empty!
'Freelance',
'Freelancer.com',
'Upwork',
'Self-Employed',
'Self Employed',
'Self-employed',
'Self employed',
'Stealth Startup',
'Sole Proprietor'
]
