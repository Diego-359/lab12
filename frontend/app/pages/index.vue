<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <nav class="flex items-center justify-between p-6 bg-white shadow-sm">
      <div class="text-2xl font-bold text-blue-600">Hogar Limpio</div>
      <div class="space-x-4">
        <NuxtLink to="/login" class="text-gray-600 hover:text-blue-600">Iniciar Sesión</NuxtLink>
        <NuxtLink to="/signup" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Empezar</NuxtLink>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="max-w-6xl mx-auto mt-16 px-6 text-center">
      <h1 class="text-5xl font-extrabold text-gray-900 mb-6">
        Tu hogar impecable, <span class="text-blue-600">con confianza.</span>
      </h1>
      <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
        Conectamos a familias en Sucre con personal de limpieza verificado y calificado. Seguridad y calidad en un solo clic.
      </p>
      <div class="flex justify-center space-x-4">
        <NuxtLink to="/signup" class="px-8 py-4 bg-blue-600 text-white rounded-xl text-lg font-semibold shadow-lg hover:bg-blue-700">
          Contratar Servicio
        </NuxtLink>
        <NuxtLink to="/signup" class="px-8 py-4 border-2 border-blue-600 text-blue-600 rounded-xl text-lg font-semibold hover:bg-blue-50">
          Quiero Trabajar
        </NuxtLink>
      </div>
    </main>
  </div>
</template>