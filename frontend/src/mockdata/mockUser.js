const mockUsers = [
  {
    id: 'user-org-123',
    email: 'organizer@hcmut.edu.vn', 
    password: 'password123',
    display_name: 'BAN TỔ CHỨC',
    type: 'ORGANIZER',
  },
  {
    id: 'user-vol-456',
    email: 'volunteer@hcmut.edu.vn',
    password: 'password123',
    display_name: 'TÌNH NGUYỆN VIÊN',
    type: 'VOLUNTEER',
  },
  {
    id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    email: 'nguyenminhquan@hcmut.edu.vn',
    password: 'password123',
    display_name: 'NGUYỄN MINH QUÂN',
    type: 'VOLUNTEER',
  },
];

export const findUserByCredentials = (email, password) => {
  const user = mockUsers.find(
    (user) => user.email.toLowerCase() === email.toLowerCase() && user.password === password
  );

  if (user) {
    const {password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }
  
  return null; 
};

export const getUserDisplayName = (id) => {
  const user = mockUsers.find((user) => user.id === id);

  if (user) {
    return user.display_name;
  }

  return '';
}