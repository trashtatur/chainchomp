#VERIFIER

##SHOULD SUCCEED
- Valid config
- valid rabbitmq profile
- valid kafka profile

##SHOULD FAIL
- no "next link" provided
- no "name" provided
- no "MQ Type" provided

#MERGER

##SHOULD SUCCEED:

- a minimal config and a maximum config (filled out wise)
- two configs that are the same
- no external config provided (should throw exception but still go through)
- one config with no profiles
- one config with two different profiles

##SHOULD FAIL:

- a profile that does not exist externally provided ( -> Should throw exception asking to install ! )
- profile provided inside config file ( -> should point to installing the profile )
- non existing mq type provided

# BUILDER

## SHOULD SUCCEED
- existing helper provided
- existing helper has functions
- string contains {{ and }} but isn't a jinja string (will keep raw data)
- No helper provided but also no functions
- Helper provided but no functions used
- No helper provided but functions there ( keep raw data )

## SHOULD FAIL
- Helper provided but functions not in helper
