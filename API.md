# API Reference <a name="API Reference" id="api-reference"></a>

## Constructs <a name="Constructs" id="Constructs"></a>

### MetaflowEventLambdaConstruct <a name="MetaflowEventLambdaConstruct" id="cdk-mf.MetaflowEventLambdaConstruct"></a>

#### Initializers <a name="Initializers" id="cdk-mf.MetaflowEventLambdaConstruct.Initializer"></a>

```typescript
import { MetaflowEventLambdaConstruct } from 'cdk-mf'

new MetaflowEventLambdaConstruct(scope: Construct, id: string, props: ICustomProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.scope">scope</a></code> | <code>constructs.Construct</code> | *No description.* |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.id">id</a></code> | <code>string</code> | *No description.* |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.props">props</a></code> | <code><a href="#cdk-mf.ICustomProps">ICustomProps</a></code> | *No description.* |

---

##### `scope`<sup>Required</sup> <a name="scope" id="cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.scope"></a>

- *Type:* constructs.Construct

---

##### `id`<sup>Required</sup> <a name="id" id="cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.id"></a>

- *Type:* string

---

##### `props`<sup>Required</sup> <a name="props" id="cdk-mf.MetaflowEventLambdaConstruct.Initializer.parameter.props"></a>

- *Type:* <a href="#cdk-mf.ICustomProps">ICustomProps</a>

---

#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.toString">toString</a></code> | Returns a string representation of this construct. |

---

##### `toString` <a name="toString" id="cdk-mf.MetaflowEventLambdaConstruct.toString"></a>

```typescript
public toString(): string
```

Returns a string representation of this construct.

#### Static Functions <a name="Static Functions" id="Static Functions"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.isConstruct">isConstruct</a></code> | Checks if `x` is a construct. |

---

##### ~~`isConstruct`~~ <a name="isConstruct" id="cdk-mf.MetaflowEventLambdaConstruct.isConstruct"></a>

```typescript
import { MetaflowEventLambdaConstruct } from 'cdk-mf'

MetaflowEventLambdaConstruct.isConstruct(x: any)
```

Checks if `x` is a construct.

###### `x`<sup>Required</sup> <a name="x" id="cdk-mf.MetaflowEventLambdaConstruct.isConstruct.parameter.x"></a>

- *Type:* any

Any object.

---

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#cdk-mf.MetaflowEventLambdaConstruct.property.node">node</a></code> | <code>constructs.Node</code> | The tree node. |

---

##### `node`<sup>Required</sup> <a name="node" id="cdk-mf.MetaflowEventLambdaConstruct.property.node"></a>

```typescript
public readonly node: Node;
```

- *Type:* constructs.Node

The tree node.

---




## Protocols <a name="Protocols" id="Protocols"></a>

### ICustomProps <a name="ICustomProps" id="cdk-mf.ICustomProps"></a>

- *Implemented By:* <a href="#cdk-mf.ICustomProps">ICustomProps</a>


#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#cdk-mf.ICustomProps.property.name">name</a></code> | <code>string</code> | *No description.* |

---

##### `name`<sup>Required</sup> <a name="name" id="cdk-mf.ICustomProps.property.name"></a>

```typescript
public readonly name: string;
```

- *Type:* string

---

