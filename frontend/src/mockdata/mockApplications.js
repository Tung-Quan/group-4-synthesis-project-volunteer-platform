export const applicationDetails = [
  {
    id: 'APP001',
	volunteerId: 'user-vol-456',
    activityId: 'MYBK001',
    timeSent: '09:00:00 14/09/2025',
	detail: 'dummy text 01 dummy text 01 dummy text 01 dummy text 01 dummy text 01 dummy text 01',
  },
  {
    id: 'APP002',
	volunteerId: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    activityId: 'MYBK002',
    timeSent: '12:00:00 03/09/2025',
	detail: 'dummy text 02',
  },
  {
    id: 'APP003',
	volunteerId: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    activityId: 'MYBK004',
    timeSent: '20:30:00 27/10/2025',
	detail: 'dummy text 03',
  },
]

export const getApplication = (id) => {
  const application = applicationDetails.find((application) => application.id === id);
  return application ? application : null; //find() returns undefined when no elements are found
}