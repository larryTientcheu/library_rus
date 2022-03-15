/*==============================================================*/
/* Nom de SGBD :  PostgreSQL 8                                  */
/* Date de création :  15/03/2022 12:57:58 PM                   */
/*==============================================================*/


drop index BOOKS_PK;

drop table BOOKS;

drop index ASSOCIATION_2_FK;

drop index ASSOCIATION_1_FK;

drop index RENTAL_PK;

drop table RENTAL;

drop index USERS_PK;

drop table USERS;

/*==============================================================*/
/* Table : BOOKS                                                */
/*==============================================================*/
create table BOOKS (
   BID                  SERIAL               not null,
   NAME                 VARCHAR(1024)        not null,
   PRICE                NUMERIC              null,
   GENRE                VARCHAR(1024)        null,
   AUTHOR               VARCHAR(1024)        null,
   constraint PK_BOOKS primary key (BID)
);

/*==============================================================*/
/* Index : BOOKS_PK                                             */
/*==============================================================*/
create unique index BOOKS_PK on BOOKS (
BID
);

/*==============================================================*/
/* Table : RENTAL                                               */
/*==============================================================*/
create table RENTAL (
   RID                  SERIAL               not null,
   BID                  INT4                 not null,
   UID                  INT4                 not null,
   ISSUEDATE            DATE                 not null,
   PERIOD               CHAR(64000)          null,
   RETURNDATE           DATE                 not null,
   FINE                 NUMERIC              null,
   constraint PK_RENTAL primary key (RID)
);

/*==============================================================*/
/* Index : RENTAL_PK                                            */
/*==============================================================*/
create unique index RENTAL_PK on RENTAL (
RID
);

/*==============================================================*/
/* Index : ASSOCIATION_1_FK                                     */
/*==============================================================*/
create  index ASSOCIATION_1_FK on RENTAL (
UID
);

/*==============================================================*/
/* Index : ASSOCIATION_2_FK                                     */
/*==============================================================*/
create  index ASSOCIATION_2_FK on RENTAL (
BID
);

/*==============================================================*/
/* Table : USERS                                                */
/*==============================================================*/
create table USERS (
   UID                  SERIAL               not null,
   USERNAME             VARCHAR(1024)        not null,
   PASSWORD             VARCHAR(1024)        not null,
   ADMIN                BOOL                 not null,
   constraint PK_USERS primary key (UID)
);

/*==============================================================*/
/* Index : USERS_PK                                             */
/*==============================================================*/
create unique index USERS_PK on USERS (
UID
);

alter table RENTAL
   add constraint FK_RENTAL_ASSOCIATI_USERS foreign key (UID)
      references USERS (UID)
      on delete restrict on update restrict;

alter table RENTAL
   add constraint FK_RENTAL_ASSOCIATI_BOOKS foreign key (BID)
      references BOOKS (BID)
      on delete restrict on update restrict;

