<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Panel de Administración - Usuarios</h1>

    <div v-if="loadingUsers" class="text-center py-4">Cargando usuarios...</div>

    <div v-else>
        <table class="min-w-full bg-white border border-gray-300">
            <thead>
                <tr class="bg-gray-100">
                    <th class="border p-2">UID</th>
                    <th class="border p-2">Email</th>
                    <th class="border p-2">Nombre</th>
                    <th class="border p-2">Rol actual</th>
                    <th class="border p-2">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.uid">
                    <td class="border p-2 font-mono text-sm">{{ user.uid }}</td>
                    <td class="border p-2">{{ user.email }}</td>
                    <td class="border p-2">{{ user.display_name }}</td>
                    <td class="border p-2">{{ user.role }}</td>
                    <td class="border p-2">
                        <select
                            v-model="user.newRole"
                            @change="updateRole(user)"
                            class="border rounded p-1"
                        >
                            <option value="cliente">Cliente</option>
                            <option value="personal_limpieza">Personal de Limpieza</option>
                            <option value="admin">Admin</option>
                        </select>
                        
                        <button 
                            v-if="user.role !== 'admin'"
                            @click="inhabilitarUsuario(user.uid)"
                            class="ml-2 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700 text-xs"
                        >
                            Inhabilitar
                        </button>

                        <span v-else class="ml-2 text-gray-400 text-xs italic">
                            Admin Protegido
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script setup lang="ts">
interface User {
    uid: string
    email: string
    display_name: string
    role: 'cliente' | 'personal_limpieza' | 'admin'
    newRole?: 'cliente' | 'personal_limpieza' | 'admin'
}

const { userRole, getToken } = useAuth()
const router = useRouter()

const users = ref<User[]>([])
const loadingUsers = ref(false)

watch(userRole, (role) => {
    if (role === null) return
    if (role !== 'admin') {
        router.push('/')
    } else {
        fetchUsers()
    }
}, { immediate: true })

async function fetchUsers() {
    loadingUsers.value = true
    try {
        const token = await getToken()
        if (!token) throw new Error('No autenticado')
        const data = await $fetch<User[]>('https://hogar-limpio-backend.onrender.com/admin/users', {
            headers: { Authorization: `Bearer ${token}` }
        })
        users.value = data.map((u: any) => ({ ...u, newRole: u.role }))
    } catch (error) {
        console.error('Error al cargar usuarios:', error)
        alert('No se pudieron cargar los usuarios')
    } finally {
        loadingUsers.value = false
    }
}

async function updateRole(user: User) {
    if (!user.newRole || user.newRole === user.role) return

    try {
        const token = await getToken()
        if (!token) throw new Error('No autenticado')

        await $fetch(`https://hogar-limpio-backend.onrender.com/admin/users/${user.uid}/role`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: { new_role: user.newRole }
        })

        user.role = user.newRole
        alert('Rol actualizado correctamente')
    } catch (error) {
        console.error('Error al actualizar rol:', error)
        alert('Error al actualizar el rol')
        user.newRole = user.role
    }
}
async function inhabilitarUsuario(uid: string) {
    if (!confirm("¿Estás seguro de inhabilitar este perfil? Por seguridad, el usuario ya no podrá ofrecer servicios.")) return

    try {
        const token = await getToken() 
        if (!token) throw new Error('No autenticado')

        await $fetch(`https://hogar-limpio-backend.onrender.com/users/${uid}/disable`, {
            method: 'PATCH',
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        alert('Usuario inhabilitado correctamente. El Escudo de Seguridad ha sido actualizado.')
        fetchUsers() 
    } catch (error) {
        console.error('Error al inhabilitar usuario:', error)
        alert('Hubo un error al intentar inhabilitar al usuario.')
    }
}
</script>