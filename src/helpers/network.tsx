import user from "../../config/user";
import { LinkedInToken } from "react-native-linkedin";

const url = "https://cs490-project3-impression-spr2.herokuapp.com/";

export function getCallParams(body: any):any {
  return {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

export function newUser(data: any):Promise<Response> {
  return fetch(`${url}/new_user`, getCallParams(data));
}

export function linkedinLogin(authorizationCode: LinkedInToken):Promise<Response> {
  return fetch(`${url}/linkedin_login`, getCallParams({ authorization_token: authorizationCode }))
}

export function getUserInfo(email: string):Promise<Response> {
  return fetch(`${url}/get_user`, getCallParams({ email }));
}

export function getConnections(email: string):Promise<Response> {
  return fetch(
    `${url}/query_connections`,
    getCallParams({ user_email: email })
  );
}

export function newConnection(email: string):Promise<Response> {
  return fetch(
    `${url}/new_connection`,
    getCallParams({ user1_email: user.email, user2_email: email })
  );
}

export function deleteConnection(email: string):Promise<Response> {
  return fetch(
    `${url}/delete_connection`,
    getCallParams({ user1_email: user.email, user2_email: email })
  );
}

export function batchNewUsers(emails:{user1_email:string, user2_email:string}[]):Promise<Response>{
  return fetch(
    `${url}/batch_new_users`,
    getCallParams(emails)
  )
}

export function editUser(user: any):Promise<Response> {
  return fetch(`${url}/edit_user`, getCallParams(user));
}

export function uploadDocument(file: any):Promise<Response> {
  const body = new FormData();
  body.append('file', {
    uri: file.uri,
    type: `application/pdf`,
    name: file.name
  });

  body.append("email", user.email)

  return fetch(
    `${url}/upload_doc`,
    {
      method: 'POST',
      body,
    }
  )
}

export function newGroup(groupName: string, emails: string[]):Promise<Response> {
  return fetch(
    `${url}/new_group`,
    getCallParams({ emails, group_name: groupName })
  );
}

export function getGroups(email: string):Promise<Response> {
  return fetch(
    `${url}/get_groups`,
    getCallParams({ email })
  );
}

export function leaveGroup(id: number, groupName: string):Promise<Response> {
  return fetch(
    `${url}/leave_group`,
    getCallParams({ group_id: id.toString(), group_name: groupName, email: user.email} )
  );
}

export function getUserFromGroups(groupName: string):Promise<Response> {
  return fetch(
    `${url}/get_users`,
    getCallParams({ group_name: groupName })
  );
}

export function getNearbyUsers(email: string, coordinates: any):Promise<Response> {
  return fetch(
    `${url}/get_nearby_users`,
    getCallParams({ email, ...coordinates })
  )
}

export function uploadGroupDocument(file: any, groupId: number):Promise<Response> {
  const body = new FormData();
  body.append('file', {
    uri: file.uri,
    type: `application/pdf`,
    name: file.name
  });

  body.append("filename", file.name);
  body.append("groupid", groupId.toString());

  return fetch(
    `${url}/upload_group_pdf`,
    {
      method: 'POST',
      body,
    }
  )
}


export function getGroupDocuments(groupid: number):Promise<Response> {
  return fetch(
    `${url}/get_group_docs`,
    getCallParams({ groupid })
  );
}
