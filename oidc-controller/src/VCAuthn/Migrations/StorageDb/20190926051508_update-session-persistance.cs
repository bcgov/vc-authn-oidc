using Microsoft.EntityFrameworkCore.Migrations;

namespace VCAuthn.Migrations
{
    public partial class updatesessionpersistance : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "RedirectUrl",
                table: "Sessions");

            migrationBuilder.RenameColumn(
                name: "ResponseType",
                table: "Sessions",
                newName: "RequestParams");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "RequestParams",
                table: "Sessions",
                newName: "ResponseType");

            migrationBuilder.AddColumn<string>(
                name: "RedirectUrl",
                table: "Sessions",
                nullable: true);
        }
    }
}
