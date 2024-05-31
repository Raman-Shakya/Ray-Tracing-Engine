# Ray Tracing (RTX) Implementation in python
> A package for raytracing

## Includes
1. A world object
1. Object (Sphere, Plane)
1. Camera (perspective camera)
1. Material Object


## World
> A class wrapping all objects, camera and lights
``` py
from rtx_engine.world import World
```
1. constructor
    ```py
    World(
        ambient = COEFFICIENT_OF_AMBIENT_LIGHT, # determines how bright the objects are without light source default=0.3
        background = BACKGROUND_TEXTURE,        # gives background texture to the world, default=NULL, accepts np.array of image
    )
    ```

1. addObject(`object`)
    Adds a new object `object` to the world

1. addLight(x, y, z)
    Adds a new point light to the world at (`x`, `y`, `z`)

1. setCamera(`camera`)
    sets a `camera` to the world

1. render()
    renders the scene and returns a np.array of rendered image

## Material
> Describes the material type of object
```py
from rtx_engine.material import Material
```
1. color
    defines color of object
1. specularCoef
    defines coefficient of specular reflection of the object, describes how shiny the object is
1. reflective
    describes how reflective the object is
1. mapping
    describes the texture of the object
> These parameters are called in the constructor to define the object

```py
Material(
    color        = np.array([1,0,1]),
    specularCoef = 40,
    reflective   = 0.3,
    mapping      = cv2.imread('assets/texture.jpg')
)
```

## Object
> Definition of the object itself

### Sphere
> A spherical object
```py
from rtx_engine.objects.sphere import Sphere
```
1. Constructor
    ```py
    Sphere(
        center,
        radius,
        material
    )
    ```

### Plane
> A plane object
```py
from rtx_engine.objects.plane import Plane
```
1. Constructor
    ```py
    Plane(
        anchor_point,
        direction,
        material
    )
    ```

## Camera
> A perspective camera object
```py
from rtx_engine.camera.perspective_camera import Camera
```
1. Constructor
    ```py
    Camera(
        focal_point,
        look_at_direction,
        width,
        height
    )
    ```