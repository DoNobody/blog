# dgraph

> [Fast, Distributed Graph DB](https://dgraph.io) > [Doc](https://docs.dgraph.io)

## 简明教程

## 启动

> 推荐使用 docker-compose 方式：参考使用官网 docker-compose.yml 文件

## graphql 默认内省字段

```graph
type __Schema {
    types : [__Type!]!
    queryType : __Type!
    mutationType : __Type
    directives : [__Directive!]!
}

type __Type {
    kind : __TypeKind!
    name : String
    description : String

    # OBJECT and INTERFACE only
    fields (includeDeprecated : Boolean = false) : [__Field!]

    # OBJECT only
    interfaces : [__Type!]

    #INTERFACE and UNION only
    possibleTypes : [__Type!]

    # ENUM only
    enumValues (includeDeprecated : Boolean = false) : [__EnumValue!]

    #INPUT_OBJECT only
    inputFields : [__InputValue!]

    #NON_NULL and LIST only
    ofType : __Type

}

type __Field {
    name : String!
    description : String
    args : [__InputValue!]!
    type : __Type!
    isDeprecated : Boolean!
    deprecationReason : String
}

type __InputValue {
    name : String!
    description : String
    type : __Type!
    defaultValue : String
}

type __EnumValue {
    name : String!
    description : String
    isDeprecated : Boolean!
    deprecationReason : String
}

enum __TypeKind {
    SCALAR
    OBJECT
    INTERFACE
    UNION
    ENUM
    INPUT_OBJECT
    LIST
    NON_NULL
}

type __Directive {
    name : String!
    description : String
    locations : [__DirectiveLocation!]!
    args : [__InputValue!]!
}

enum __DirectiveLocation {
    QUERY
    MUTATION
    FIELD
    FRAGMENT_DEFINITION
    FRAGMENT_SPREAD
    INLINE_FRAGMENT
}
```

## 查询当前的内部结构

```graphql
# graphql query
{
  __schema {
    queryType {
      name
      kind
      description
      fields {
        name
        type {
          name
          kind
        }
        args {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
          defaultValue
          description
        }
      }
    }
    mutationType {
      name
      kind
      description
      fields {
        name
        type {
          name
          kind
        }
        args {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
          defaultValue
          description
        }
      }
    }
    directives {
      name
      description
      args {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
        defaultValue
        description
      }
    }
  }
}
```
