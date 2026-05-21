

IF DB_ID('UDEMYTEST1') IS NULL
BEGIN
    CREATE DATABASE UDEMYTEST1;
END
GO

USE UDEMYTEST1;
GO

IF OBJECT_ID('dbo.Cursos', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Cursos (
        IDCurso INT IDENTITY(1,1) PRIMARY KEY,
        NombreCurso VARCHAR(100) NOT NULL,
        Descripcion VARCHAR(250) NULL,
        DuracionHoras INT NOT NULL,
        Precio DECIMAL(10,2) NOT NULL,
        Estado BIT NOT NULL DEFAULT 1
    );
END
GO

/* Datos de prueba opcionales */
IF NOT EXISTS (SELECT 1 FROM dbo.Cursos)
BEGIN
    INSERT INTO dbo.Cursos (NombreCurso, Descripcion, DuracionHoras, Precio, Estado)
    VALUES
    ('Python Básico', 'Curso introductorio de programación en Python', 40, 49.99, 1),
    ('SQL Server', 'Curso de consultas y procedimientos almacenados', 35, 59.99, 1),
    ('Base de Datos II', 'Curso práctico de conexión entre Python y SQL Server', 50, 69.99, 1);
END
GO

/* Eliminar procedimientos si ya existen */
IF OBJECT_ID('dbo.sp_insertar_curso', 'P') IS NOT NULL DROP PROCEDURE dbo.sp_insertar_curso;
GO
IF OBJECT_ID('dbo.sp_consultar_cursos', 'P') IS NOT NULL DROP PROCEDURE dbo.sp_consultar_cursos;
GO
IF OBJECT_ID('dbo.sp_actualizar_curso', 'P') IS NOT NULL DROP PROCEDURE dbo.sp_actualizar_curso;
GO
IF OBJECT_ID('dbo.sp_eliminar_curso', 'P') IS NOT NULL DROP PROCEDURE dbo.sp_eliminar_curso;
GO
IF OBJECT_ID('dbo.sp_buscar_curso_por_id', 'P') IS NOT NULL DROP PROCEDURE dbo.sp_buscar_curso_por_id;
GO

CREATE PROCEDURE dbo.sp_insertar_curso
    @NombreCurso VARCHAR(100),
    @Descripcion VARCHAR(250),
    @DuracionHoras INT,
    @Precio DECIMAL(10,2),
    @Estado BIT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.Cursos (NombreCurso, Descripcion, DuracionHoras, Precio, Estado)
    VALUES (@NombreCurso, @Descripcion, @DuracionHoras, @Precio, @Estado);

    SELECT SCOPE_IDENTITY() AS NuevoIDCurso;
END
GO

CREATE PROCEDURE dbo.sp_consultar_cursos
AS
BEGIN
    SET NOCOUNT ON;

    SELECT IDCurso, NombreCurso, Descripcion, DuracionHoras, Precio, Estado
    FROM dbo.Cursos
    ORDER BY IDCurso;
END
GO

CREATE PROCEDURE dbo.sp_buscar_curso_por_id
    @IDCurso INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT IDCurso, NombreCurso, Descripcion, DuracionHoras, Precio, Estado
    FROM dbo.Cursos
    WHERE IDCurso = @IDCurso;
END
GO

CREATE PROCEDURE dbo.sp_actualizar_curso
    @IDCurso INT,
    @NombreCurso VARCHAR(100),
    @Descripcion VARCHAR(250),
    @DuracionHoras INT,
    @Precio DECIMAL(10,2),
    @Estado BIT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.Cursos
    SET NombreCurso = @NombreCurso,
        Descripcion = @Descripcion,
        DuracionHoras = @DuracionHoras,
        Precio = @Precio,
        Estado = @Estado
    WHERE IDCurso = @IDCurso;

    SELECT @@ROWCOUNT AS FilasAfectadas;
END
GO

CREATE PROCEDURE dbo.sp_eliminar_curso
    @IDCurso INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM dbo.Cursos
    WHERE IDCurso = @IDCurso;

    SELECT @@ROWCOUNT AS FilasAfectadas;
END
GO
