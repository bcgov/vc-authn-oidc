using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace VCAuthn.Migrations
{
    public partial class PresentationConfigs : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "MappedUrls",
                columns: table => new
                {
                    Key = table.Column<string>(nullable: false),
                    Url = table.Column<string>(nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MappedUrls", x => x.Key);
                });

            migrationBuilder.CreateTable(
                name: "PresentationConfigurations",
                columns: table => new
                {
                    Id = table.Column<string>(nullable: false),
                    SubjectIdentifier = table.Column<string>(nullable: true),
                    Config = table.Column<string>(nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PresentationConfigurations", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Sessions",
                columns: table => new
                {
                    Id = table.Column<string>(nullable: false),
                    PresentationRequestId = table.Column<string>(nullable: true),
                    ExpiredTimestamp = table.Column<DateTime>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Sessions", x => x.Id);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "MappedUrls");

            migrationBuilder.DropTable(
                name: "PresentationConfigurations");

            migrationBuilder.DropTable(
                name: "Sessions");
        }
    }
}
