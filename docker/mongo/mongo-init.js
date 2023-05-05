db.createUser({
  user: "oidccontrolleruser",
  pwd: "oidccontrollerpass",
  roles: [
    {
      role: "readWrite",
      db: "oidccontroller",
    },
  ],
});
