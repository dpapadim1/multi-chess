<!DOCTYPE html>

<html lang="en">

    <head>

        <meta charset="utf-8">
        <meta name="viewport" content="initial-scale=1, width=device-width">

        <!-- http://getbootstrap.com/docs/5.3/ -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

        <!-- https://favicon.io/emoji-favicons/money-bag/ -->
        <link href="/static/favicon.ico" rel="icon">

        <link href="/static/styles.css" rel="stylesheet">

        <title>Multi-Chess: 
    Log In
</title>

    </head>

    <body>

        <nav class="bg-light border navbar navbar-expand-md navbar-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="/"><span class="blue">Multi</span><span class="red">Chess</span></a>
                <button aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbar" data-bs-toggle="collapse" type="button">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbar">
                    
                        <ul class="navbar-nav ms-auto mt-2">
                            <li class="nav-item"><a class="nav-link" href="/register">Register</a></li>
                            <li class="nav-item"><a class="nav-link" href="/login">Log In</a></li>
                        </ul>
                    
                </div>
            </div>
        </nav>

        

        <main class="container py-5 text-center">
            
    <form action="/login" method="post">
        <div class="mb-3">
            <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="username" placeholder="Username" type="text">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="password" placeholder="Password" type="password">
        </div>
        <button class="btn btn-primary" type="submit">Log In</button>
    </form>

        </main>

    </body>

</html>